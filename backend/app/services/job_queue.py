import asyncio
from dataclasses import dataclass
from uuid import uuid4

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.serializers import JSONSerializer

from app.config import Settings
from app.schemas import JobStatus, JobSubmission
from app.services.jobs import execute_job, run_job


class JobNotFoundError(RuntimeError):
    pass


class QueueBackend:
    async def enqueue(self, job_type: str, payload: dict[str, object]) -> JobSubmission:
        raise NotImplementedError

    async def get(self, job_id: str) -> JobStatus:
        raise NotImplementedError


@dataclass
class MemoryJob:
    id: str
    type: str
    status: str = "queued"
    result: dict[str, object] | None = None
    error: str | None = None


_MEMORY_JOBS: dict[str, MemoryJob] = {}
_MEMORY_TASKS: set[asyncio.Task[None]] = set()


class InMemoryQueueBackend(QueueBackend):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def enqueue(self, job_type: str, payload: dict[str, object]) -> JobSubmission:
        job = MemoryJob(id=uuid4().hex, type=job_type)
        _MEMORY_JOBS[job.id] = job
        task = asyncio.create_task(self._execute(job, payload))
        _MEMORY_TASKS.add(task)
        task.add_done_callback(_MEMORY_TASKS.discard)
        return JobSubmission(id=job.id, status=job.status)

    async def _execute(self, job: MemoryJob, payload: dict[str, object]) -> None:
        job.status = "started"
        try:
            job.result = await execute_job(job.type, payload, self.settings)
            job.status = "finished"
        except Exception as exc:
            job.status = "failed"
            job.error = str(exc) or "Job failed"

    async def get(self, job_id: str) -> JobStatus:
        job = _MEMORY_JOBS.get(job_id)
        if job is None:
            raise JobNotFoundError("Job not found")
        return JobStatus(
            id=job.id,
            type=job.type,
            status=job.status,
            result=job.result,
            error=job.error,
        )


class RQQueueBackend(QueueBackend):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.connection = Redis.from_url(settings.redis_url)

    async def enqueue(self, job_type: str, payload: dict[str, object]) -> JobSubmission:
        queue = Queue(
            f"{self.settings.queue_name}-{job_type}",
            connection=self.connection,
            serializer=JSONSerializer,
        )
        job = await asyncio.to_thread(
            queue.enqueue,
            run_job,
            job_type,
            payload,
            job_timeout=self.settings.queue_job_timeout_seconds,
            result_ttl=86_400,
            failure_ttl=86_400,
            meta={"type": job_type},
        )
        return JobSubmission(id=job.id, status="queued")

    async def get(self, job_id: str) -> JobStatus:
        try:
            job = await asyncio.to_thread(
                Job.fetch,
                job_id,
                connection=self.connection,
                serializer=JSONSerializer,
            )
        except Exception as exc:
            raise JobNotFoundError("Job not found") from exc
        status = await asyncio.to_thread(job.get_status, refresh=True)
        status_value = status.value if hasattr(status, "value") else str(status)
        return JobStatus(
            id=job.id,
            type=str(job.meta.get("type", "unknown")),
            status=status_value,
            result=job.result if status_value == "finished" else None,
            error="Job failed" if status_value == "failed" else None,
        )


def create_queue_backend(settings: Settings) -> QueueBackend:
    if settings.queue_backend == "memory":
        return InMemoryQueueBackend(settings)
    if settings.queue_backend == "redis":
        return RQQueueBackend(settings)
    raise ValueError("QUEUE_BACKEND must be 'memory' or 'redis'")

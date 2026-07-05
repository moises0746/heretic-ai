import asyncio

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app
from app.schemas import JobStatus, JobSubmission
from app.services import job_queue
from app.services.job_queue import InMemoryQueueBackend, QueueBackend, RQQueueBackend


@pytest.mark.asyncio
async def test_memory_queue_completes_job(monkeypatch: pytest.MonkeyPatch) -> None:
    async def execute(
        job_type: str,
        payload: dict[str, object],
        settings: Settings,
    ) -> dict[str, object]:
        return {"job_type": job_type, "payload": payload}

    monkeypatch.setattr(job_queue, "execute_job", execute)
    backend = InMemoryQueueBackend(Settings())

    submission = await backend.enqueue("images", {"seed": 7})
    await asyncio.sleep(0)
    status = await backend.get(submission.id)

    assert status.status == "finished"
    assert status.result == {"job_type": "images", "payload": {"seed": 7}}


@pytest.mark.asyncio
async def test_memory_queue_records_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fail(
        job_type: str,
        payload: dict[str, object],
        settings: Settings,
    ) -> dict[str, object]:
        raise RuntimeError("Generation failed")

    monkeypatch.setattr(job_queue, "execute_job", fail)
    backend = InMemoryQueueBackend(Settings())

    submission = await backend.enqueue("video", {})
    await asyncio.sleep(0)
    status = await backend.get(submission.id)

    assert status.status == "failed"
    assert status.error == "Generation failed"


class FakeQueueBackend(QueueBackend):
    async def enqueue(self, job_type: str, payload: dict[str, object]) -> JobSubmission:
        return JobSubmission(id="queued-job", status="queued")

    async def get(self, job_id: str) -> JobStatus:
        return JobStatus(
            id=job_id,
            type="images",
            status="finished",
            result={"images": []},
        )


def test_job_api_enqueues_and_reads_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.main.create_queue_backend", lambda settings: FakeQueueBackend())
    client = TestClient(app)
    scene = {
        "narration": "Narration.",
        "image_prompt": "A detailed cinematic image.",
        "duration_seconds": 30,
    }

    submission = client.post("/api/v1/jobs/images", json={"scenes": [scene]})
    status = client.get("/api/v1/jobs/queued-job")

    assert submission.status_code == 202
    assert submission.json() == {"id": "queued-job", "status": "queued"}
    assert status.status_code == 200
    assert status.json()["result"] == {"images": []}


@pytest.mark.asyncio
async def test_rq_uses_workload_specific_queue(monkeypatch: pytest.MonkeyPatch) -> None:
    queue_names: list[str] = []

    class FakeJob:
        id = "redis-job"

    class FakeQueue:
        def __init__(self, name: str, **kwargs: object) -> None:
            queue_names.append(name)

        def enqueue(self, *args: object, **kwargs: object) -> FakeJob:
            return FakeJob()

    monkeypatch.setattr(job_queue, "Queue", FakeQueue)
    backend = RQQueueBackend(Settings(queue_name="heretic"))

    submission = await backend.enqueue("audio", {"voice_profile_id": "a" * 32})

    assert submission.id == "redis-job"
    assert queue_names == ["heretic-audio"]

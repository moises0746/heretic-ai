type JobStatus<T> = {
  id: string;
  status: "queued" | "started" | "finished" | "failed";
  result?: T;
  error?: string;
};

function delay(milliseconds: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

async function readJson(response: Response): Promise<Record<string, unknown>> {
  try {
    return await response.json();
  } catch {
    return {};
  }
}

export async function runQueuedJob<T>(
  apiBaseUrl: string,
  jobType: "audio" | "images" | "video",
  payload: object,
  pollIntervalMs = 1000,
  maxPolls = 3600,
): Promise<T> {
  const submissionResponse = await fetch(`${apiBaseUrl}/api/v1/jobs/${jobType}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const submission = await readJson(submissionResponse);
  if (!submissionResponse.ok) {
    throw new Error(String(submission.detail ?? "Could not enqueue job"));
  }
  const jobId = String(submission.id);

  for (let attempt = 0; attempt < maxPolls; attempt += 1) {
    const statusResponse = await fetch(`${apiBaseUrl}/api/v1/jobs/${jobId}`);
    const status = (await readJson(statusResponse)) as JobStatus<T>;
    if (!statusResponse.ok) {
      throw new Error(String((status as Record<string, unknown>).detail ?? "Could not read job status"));
    }
    if (status.status === "finished" && status.result) return status.result;
    if (status.status === "failed") throw new Error(status.error ?? "Job failed");
    await delay(pollIntervalMs);
  }
  throw new Error("Job status polling timed out");
}


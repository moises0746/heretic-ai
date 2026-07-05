"use client";

import { FormEvent, useState } from "react";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [script, setScript] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setScript("");
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/scripts/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, duration_seconds: 60 }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Script generation failed");
      setScript(data.script);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <section className="hero">
        <p className="eyebrow">SELF-HOSTED VIDEO LAB</p>
        <h1>Turn one idea into a production-ready script.</h1>
        <p className="subtitle">The first working slice of the local AI video pipeline.</p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="prompt">Video topic</label>
          <textarea
            id="prompt"
            minLength={3}
            maxLength={2000}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Explain how solar storms affect modern infrastructure"
            required
            rows={5}
            value={prompt}
          />
          <button disabled={isLoading || prompt.trim().length < 3} type="submit">
            {isLoading ? "Generating…" : "Generate 60-second script"}
          </button>
        </form>

        {error && <p className="message error">{error}</p>}
        {script && (
          <article className="result">
            <h2>Generated script</h2>
            <p>{script}</p>
          </article>
        )}
      </section>
    </main>
  );
}


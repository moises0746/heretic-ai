"use client";

import { FormEvent, useState } from "react";
import Image from "next/image";
import VoicePanel from "./voice-panel";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type Scene = {
  narration: string;
  image_prompt: string;
  duration_seconds: number;
};

type VideoPlan = {
  title: string;
  scenes: Scene[];
  model: string;
};

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [videoPlan, setVideoPlan] = useState<VideoPlan | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setVideoPlan(null);
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/scripts/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, duration_seconds: 60 }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Script generation failed");
      setVideoPlan(data as VideoPlan);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <section className="hero">
        <header className="brand" aria-label="Heretic home">
          <Image className="brand-mark" src="/heretic-mark.svg" alt="" width={48} height={48} priority />
          <span className="brand-name">Heretic</span>
        </header>
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

        {error && <p className="message error" role="alert">{error}</p>}
        {videoPlan && (
          <article className="result">
            <div className="result-heading">
              <div>
                <p className="result-label">Generated video plan</p>
                <h2>{videoPlan.title}</h2>
              </div>
              <span>{videoPlan.scenes.length} scenes</span>
            </div>
            <ol className="scene-list">
              {videoPlan.scenes.map((scene, index) => (
                <li className="scene" key={`${index}-${scene.narration}`}>
                  <div className="scene-heading">
                    <h3>Scene {index + 1}</h3>
                    <span>{scene.duration_seconds}s</span>
                  </div>
                  <p>{scene.narration}</p>
                  <p className="image-prompt"><strong>Visual:</strong> {scene.image_prompt}</p>
                </li>
              ))}
            </ol>
            <VoicePanel apiBaseUrl={apiBaseUrl} scenes={videoPlan.scenes} />
          </article>
        )}
      </section>
    </main>
  );
}


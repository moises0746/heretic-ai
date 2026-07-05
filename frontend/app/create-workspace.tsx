"use client";

import { FormEvent, useState } from "react";
import ImagePanel from "./image-panel";
import RenderPanel from "./render-panel";
import VoicePanel from "./voice-panel";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type Scene = { narration: string; image_prompt: string; duration_seconds: number };
type VideoPlan = { title: string; scenes: Scene[]; model: string };
type AudioAsset = { scene_index: number; path: string; url: string };
type ImageAsset = { scene_index: number; prompt: string; seed: number; path: string; url: string };

const steps = ["Story plan", "Narration", "Scene images", "Render"];

export default function CreateWorkspace() {
  const [prompt, setPrompt] = useState("");
  const [videoPlan, setVideoPlan] = useState<VideoPlan | null>(null);
  const [audioAssets, setAudioAssets] = useState<AudioAsset[]>([]);
  const [imageAssets, setImageAssets] = useState<ImageAsset[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(""); setVideoPlan(null); setAudioAssets([]); setImageAssets([]); setIsLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/scripts/generate`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, duration_seconds: 60 }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Script generation failed");
      setVideoPlan(data as VideoPlan);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally { setIsLoading(false); }
  }

  return (
    <div className="create-page">
      <header className="workspace-heading">
        <div><p className="eyebrow">VIDEO STUDIO</p><h1>Create a complete video</h1><p>Start with one idea, then guide each local generation step through export.</p></div>
        <span className="status-badge ready">Pipeline ready</span>
      </header>
      <ol className="create-steps" aria-label="Video workflow">
        {steps.map((step, index) => <li className={index === 0 ? "active" : ""} key={step}><span>{index + 1}</span>{step}</li>)}
      </ol>
      <section className="prompt-card">
        <div className="prompt-intro"><span>01</span><div><h2>Describe your video</h2><p>Heretic will turn this into a structured 60-second scene plan.</p></div></div>
        <form className="prompt-form" onSubmit={handleSubmit}>
          <label htmlFor="prompt">Video topic</label>
          <textarea id="prompt" minLength={3} maxLength={2000} onChange={(event) => setPrompt(event.target.value)} placeholder="Explain how solar storms affect modern infrastructure" required rows={5} value={prompt} />
          <div className="prompt-footer"><small>{prompt.length} / 2,000</small><button disabled={isLoading || prompt.trim().length < 3} type="submit">{isLoading ? "Generating..." : "Generate story plan"}<span aria-hidden="true">→</span></button></div>
        </form>
      </section>
      {error && <p className="message error" role="alert">{error}</p>}
      {videoPlan && (
        <article className="result">
          <div className="result-heading"><div><p className="result-label">Generated video plan</p><h2>{videoPlan.title}</h2></div><span>{videoPlan.scenes.length} scenes</span></div>
          <ol className="scene-list">{videoPlan.scenes.map((scene, index) => (
            <li className="scene" key={`${index}-${scene.narration}`}><div className="scene-heading"><h3>Scene {index + 1}</h3><span>{scene.duration_seconds}s</span></div><p>{scene.narration}</p><p className="image-prompt"><strong>Visual:</strong> {scene.image_prompt}</p></li>
          ))}</ol>
          <VoicePanel apiBaseUrl={apiBaseUrl} scenes={videoPlan.scenes} onGenerated={setAudioAssets} />
          <ImagePanel apiBaseUrl={apiBaseUrl} scenes={videoPlan.scenes} onGenerated={setImageAssets} />
          <RenderPanel apiBaseUrl={apiBaseUrl} title={videoPlan.title} scenes={videoPlan.scenes} audio={audioAssets} images={imageAssets} />
        </article>
      )}
    </div>
  );
}

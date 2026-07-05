"use client";

import { useState } from "react";
import { runQueuedJob } from "../lib/jobs";

type Scene = {
  narration: string;
  image_prompt: string;
  duration_seconds: number;
};

type AudioAsset = {
  scene_index: number;
  path: string;
  url: string;
};

type ImageAsset = {
  scene_index: number;
  prompt: string;
  seed: number;
  path: string;
  url: string;
};

type RenderResult = {
  video_url: string;
  subtitle_url: string;
};

type RenderPanelProps = {
  apiBaseUrl: string;
  title: string;
  scenes: Scene[];
  audio: AudioAsset[];
  images: ImageAsset[];
};

export default function RenderPanel({
  apiBaseUrl,
  title,
  scenes,
  audio,
  images,
}: RenderPanelProps) {
  const [result, setResult] = useState<RenderResult | null>(null);
  const [error, setError] = useState("");
  const [isRendering, setIsRendering] = useState(false);
  const isReady = audio.length === scenes.length && images.length === scenes.length;

  async function renderVideo() {
    setError("");
    setResult(null);
    setIsRendering(true);
    try {
      const renderResult = await runQueuedJob<RenderResult>(
        apiBaseUrl,
        "video",
        { title, scenes, audio, images, width: 1280, height: 720 },
      );
      setResult(renderResult);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsRendering(false);
    }
  }

  return (
    <section className="render-panel" aria-labelledby="render-heading">
      <div className="panel-heading">
        <div>
          <p className="result-label">Phase 4</p>
          <h2 id="render-heading">Assemble video</h2>
          <p className="panel-copy">
            {isReady
              ? "Audio and images are ready for every scene."
              : `Ready when ${scenes.length} audio clips and ${scenes.length} images are generated.`}
          </p>
        </div>
        <button disabled={!isReady || isRendering} onClick={renderVideo} type="button">
          {isRendering ? "Rendering MP4..." : "Render MP4"}
        </button>
      </div>

      {error && <p className="message error" role="alert">{error}</p>}
      {result && (
        <div className="video-result">
          <video controls preload="metadata" src={`${apiBaseUrl}${result.video_url}`}>
            Your browser does not support video playback.
          </video>
          <div className="download-links">
            <a href={`${apiBaseUrl}${result.video_url}`} download>Download MP4</a>
            <a href={`${apiBaseUrl}${result.subtitle_url}`} download>Download SRT</a>
          </div>
        </div>
      )}
    </section>
  );
}

"use client";

import { useState } from "react";

type Scene = {
  narration: string;
  image_prompt: string;
  duration_seconds: number;
};

type ImageAsset = {
  scene_index: number;
  prompt: string;
  seed: number;
  path: string;
  url: string;
};

type ImagePanelProps = {
  apiBaseUrl: string;
  scenes: Scene[];
};

export default function ImagePanel({ apiBaseUrl, scenes }: ImagePanelProps) {
  const [images, setImages] = useState<ImageAsset[]>([]);
  const [error, setError] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  async function generateImages() {
    setError("");
    setImages([]);
    setIsGenerating(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/images/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenes, width: 1280, height: 720, seed: 0 }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.detail ?? "Image generation failed");
      setImages(result.images);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <section className="image-panel" aria-labelledby="image-heading">
      <div className="panel-heading">
        <div>
          <p className="result-label">Phase 3</p>
          <h2 id="image-heading">Generate scene images</h2>
          <p className="panel-copy">Create one deterministic 16:9 image from each visual prompt.</p>
        </div>
        <button disabled={isGenerating} onClick={generateImages} type="button">
          {isGenerating ? "Generating images..." : "Generate images"}
        </button>
      </div>

      {error && <p className="message error" role="alert">{error}</p>}
      {images.length > 0 && (
        <ol className="image-grid">
          {images.map((image) => (
            <li key={image.path}>
              {/* Generated images are served by the configurable local backend URL. */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={`${apiBaseUrl}${image.url}`} alt={image.prompt} />
              <div>
                <strong>Scene {image.scene_index}</strong>
                <span>Seed {image.seed}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}


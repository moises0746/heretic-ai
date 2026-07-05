"use client";

import { FormEvent, useEffect, useState } from "react";
import { runQueuedJob } from "../lib/jobs";

type Scene = {
  narration: string;
  image_prompt: string;
  duration_seconds: number;
};

type VoiceProfile = {
  id: string;
  name: string;
};

type AudioAsset = {
  scene_index: number;
  path: string;
  url: string;
};

type VoicePanelProps = {
  apiBaseUrl: string;
  scenes: Scene[];
  onGenerated?: (audio: AudioAsset[]) => void;
};

export default function VoicePanel({ apiBaseUrl, scenes, onGenerated }: VoicePanelProps) {
  const [voices, setVoices] = useState<VoiceProfile[]>([]);
  const [selectedVoiceId, setSelectedVoiceId] = useState("");
  const [audio, setAudio] = useState<AudioAsset[]>([]);
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    let isActive = true;
    fetch(`${apiBaseUrl}/api/v1/voices`)
      .then(async (response) => {
        if (!response.ok) throw new Error("Could not load voice profiles");
        return response.json() as Promise<VoiceProfile[]>;
      })
      .then((profiles) => {
        if (!isActive) return;
        setVoices(profiles);
        setSelectedVoiceId((current) => current || profiles[0]?.id || "");
      })
      .catch((requestError: unknown) => {
        if (isActive) {
          setError(requestError instanceof Error ? requestError.message : "Unexpected error");
        }
      });
    return () => {
      isActive = false;
    };
  }, [apiBaseUrl]);

  async function uploadVoice(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsUploading(true);
    const form = event.currentTarget;
    const formData = new FormData(form);

    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/voices`, {
        method: "POST",
        body: formData,
      });
      const profile = await response.json();
      if (!response.ok) throw new Error(profile.detail ?? "Voice upload failed");
      setVoices((current) => [...current, profile]);
      setSelectedVoiceId(profile.id);
      form.reset();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsUploading(false);
    }
  }

  async function generateAudio() {
    setError("");
    setAudio([]);
    onGenerated?.([]);
    setIsGenerating(true);
    try {
      const result = await runQueuedJob<{ audio: AudioAsset[] }>(
        apiBaseUrl,
        "audio",
        { voice_profile_id: selectedVoiceId, scenes },
      );
      setAudio(result.audio);
      onGenerated?.(result.audio);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unexpected error");
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <section className="voice-panel" aria-labelledby="voice-heading">
      <div>
        <p className="result-label">Phase 2</p>
        <h2 id="voice-heading">Add narration</h2>
        <p className="panel-copy">Upload a short reference recording and its exact transcript.</p>
      </div>

      <form className="voice-form" onSubmit={uploadVoice}>
        <label htmlFor="voice-name">Voice name</label>
        <input id="voice-name" name="name" maxLength={80} required />
        <label htmlFor="reference-text">Reference transcript</label>
        <textarea id="reference-text" name="reference_text" maxLength={1000} rows={3} required />
        <label htmlFor="reference-audio">Reference audio</label>
        <input
          id="reference-audio"
          name="reference_audio"
          type="file"
          accept="audio/wav,audio/flac,audio/mpeg,audio/mp4"
          required
        />
        <button disabled={isUploading} type="submit">
          {isUploading ? "Uploading..." : "Save voice profile"}
        </button>
      </form>

      {voices.length > 0 && (
        <div className="generate-audio">
          <label htmlFor="voice-profile">Narration voice</label>
          <select
            id="voice-profile"
            value={selectedVoiceId}
            onChange={(event) => setSelectedVoiceId(event.target.value)}
          >
            {voices.map((voice) => (
              <option key={voice.id} value={voice.id}>{voice.name}</option>
            ))}
          </select>
          <button disabled={!selectedVoiceId || isGenerating} onClick={generateAudio} type="button">
            {isGenerating ? "Generating audio..." : "Generate narration"}
          </button>
        </div>
      )}

      {error && <p className="message error" role="alert">{error}</p>}
      {audio.length > 0 && (
        <ol className="audio-list">
          {audio.map((asset) => (
            <li key={asset.path}>
              <span>Scene {asset.scene_index}</span>
              <audio controls preload="metadata" src={`${apiBaseUrl}${asset.url}`}>
                Your browser does not support audio playback.
              </audio>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}

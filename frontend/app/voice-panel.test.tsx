import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import VoicePanel from "./voice-panel";

const scenes = [
  {
    narration: "Scene narration.",
    image_prompt: "A detailed cinematic scene.",
    duration_seconds: 60,
  },
];

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("VoicePanel", () => {
  it("loads a voice and renders generated scene audio", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [{ id: "a".repeat(32), name: "Narrator" }],
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            job_id: "job-1",
            audio: [{ scene_index: 1, path: "audio/job-1/scene-001.wav", url: "/media/audio/job-1/scene-001.wav" }],
          }),
        }),
    );
    const { container } = render(
      <VoicePanel apiBaseUrl="http://127.0.0.1:8000" scenes={scenes} />,
    );

    fireEvent.click(await screen.findByRole("button", { name: "Generate narration" }));

    expect(await screen.findByText("Scene 1")).toBeInTheDocument();
    expect(container.querySelector("audio")).toHaveAttribute(
      "src",
      "http://127.0.0.1:8000/media/audio/job-1/scene-001.wav",
    );
  });

  it("shows a voice loading error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, json: async () => ({}) }),
    );

    render(<VoicePanel apiBaseUrl="http://127.0.0.1:8000" scenes={scenes} />);

    expect(await screen.findByRole("alert")).toHaveTextContent("Could not load voice profiles");
  });
});


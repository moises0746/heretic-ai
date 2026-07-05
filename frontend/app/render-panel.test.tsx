import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import RenderPanel from "./render-panel";

const scenes = [
  {
    narration: "Scene narration.",
    image_prompt: "A cinematic violet city at night.",
    duration_seconds: 60,
  },
];
const audio = [{ scene_index: 1, path: "audio/job/scene.wav", url: "/media/audio/job/scene.wav" }];
const images = [
  {
    scene_index: 1,
    prompt: scenes[0].image_prompt,
    seed: 0,
    path: "images/job/scene.png",
    url: "/media/images/job/scene.png",
  },
];

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("RenderPanel", () => {
  it("stays disabled until all scene assets are ready", () => {
    render(
      <RenderPanel
        apiBaseUrl="http://127.0.0.1:8000"
        title="Test"
        scenes={scenes}
        audio={[]}
        images={[]}
      />,
    );

    expect(screen.getByRole("button", { name: "Render MP4" })).toBeDisabled();
  });

  it("renders video and subtitle download links", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ id: "video-job", status: "queued" }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            id: "video-job",
            status: "finished",
            result: {
              video_url: "/media/videos/job/video.mp4",
              subtitle_url: "/media/videos/job/subtitles.srt",
            },
          }),
        }),
    );
    const { container } = render(
      <RenderPanel
        apiBaseUrl="http://127.0.0.1:8000"
        title="Test"
        scenes={scenes}
        audio={audio}
        images={images}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Render MP4" }));

    expect(await screen.findByRole("link", { name: "Download MP4" })).toHaveAttribute(
      "href",
      "http://127.0.0.1:8000/media/videos/job/video.mp4",
    );
    expect(container.querySelector("video")).toHaveAttribute(
      "src",
      "http://127.0.0.1:8000/media/videos/job/video.mp4",
    );
  });
});

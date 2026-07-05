import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import ImagePanel from "./image-panel";

const scenes = [
  {
    narration: "Scene narration.",
    image_prompt: "A cinematic violet city at night.",
    duration_seconds: 60,
  },
];

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("ImagePanel", () => {
  it("renders images returned by the local API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          job_id: "image-job",
          images: [
            {
              scene_index: 1,
              prompt: scenes[0].image_prompt,
              seed: 0,
              path: "images/image-job/scene-001.png",
              url: "/media/images/image-job/scene-001.png",
            },
          ],
        }),
      }),
    );
    const { container } = render(
      <ImagePanel apiBaseUrl="http://127.0.0.1:8000" scenes={scenes} />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Generate images" }));

    expect(await screen.findByText("Scene 1")).toBeInTheDocument();
    expect(container.querySelector("img")).toHaveAttribute(
      "src",
      "http://127.0.0.1:8000/media/images/image-job/scene-001.png",
    );
  });

  it("shows a generation error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "FLUX runtime is unavailable" }),
      }),
    );
    render(<ImagePanel apiBaseUrl="http://127.0.0.1:8000" scenes={scenes} />);

    fireEvent.click(screen.getByRole("button", { name: "Generate images" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("FLUX runtime is unavailable");
  });
});


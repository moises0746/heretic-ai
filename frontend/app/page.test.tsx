import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import Home from "./page";

const videoPlan = {
  title: "Solar Storms Explained",
  scenes: [
    {
      narration: "A solar storm begins with an eruption from the Sun.",
      image_prompt: "A cinematic solar flare erupting into deep space",
      duration_seconds: 60,
    },
  ],
  model: "qwen3:1.7b",
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("Home", () => {
  it("renders the Heretic brand and prompt form", () => {
    render(<Home />);

    expect(screen.getByText("Heretic")).toBeInTheDocument();
    expect(screen.getByLabelText("Video topic")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate 60-second script" })).toBeDisabled();
  });

  it("renders a structured video plan returned by the API", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => videoPlan,
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });
    vi.stubGlobal(
      "fetch",
      fetchMock,
    );
    render(<Home />);

    fireEvent.change(screen.getByLabelText("Video topic"), {
      target: { value: "Solar storms" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Generate 60-second script" }));

    expect(await screen.findByRole("heading", { name: videoPlan.title })).toBeInTheDocument();
    expect(screen.getByText(videoPlan.scenes[0].narration)).toBeInTheDocument();
    expect(screen.getByText(/cinematic solar flare/)).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Add narration" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Generate scene images" })).toBeInTheDocument();
  });

  it("shows an API error and restores the submit button", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "Ollama is unavailable" }),
      }),
    );
    render(<Home />);

    fireEvent.change(screen.getByLabelText("Video topic"), {
      target: { value: "Solar storms" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Generate 60-second script" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Ollama is unavailable");
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Generate 60-second script" })).toBeEnabled();
    });
  });
});

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import CreateWorkspace from "./create-workspace";

const videoPlan = {
  title: "Solar Storms Explained",
  scenes: [{ narration: "A solar storm begins with an eruption from the Sun.", image_prompt: "A cinematic solar flare erupting into deep space", duration_seconds: 60 }],
  model: "qwen3:1.7b",
};

afterEach(() => { vi.unstubAllGlobals(); });

describe("CreateWorkspace", () => {
  it("renders the guided prompt form", () => {
    render(<CreateWorkspace />);
    expect(screen.getByRole("heading", { name: "Create a complete video" })).toBeInTheDocument();
    expect(screen.getByLabelText("Video topic")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Generate story plan/ })).toBeDisabled();
  });

  it("renders a structured video plan returned by the API", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce({ ok: true, json: async () => videoPlan }).mockResolvedValueOnce({ ok: true, json: async () => [] }));
    render(<CreateWorkspace />);
    fireEvent.change(screen.getByLabelText("Video topic"), { target: { value: "Solar storms" } });
    fireEvent.click(screen.getByRole("button", { name: /Generate story plan/ }));

    expect(await screen.findByRole("heading", { name: videoPlan.title })).toBeInTheDocument();
    expect(screen.getByText(videoPlan.scenes[0].narration)).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Add narration" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Generate scene images" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Assemble video" })).toBeInTheDocument();
  });

  it("shows an API error and restores the submit button", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, json: async () => ({ detail: "Ollama is unavailable" }) }));
    render(<CreateWorkspace />);
    fireEvent.change(screen.getByLabelText("Video topic"), { target: { value: "Solar storms" } });
    fireEvent.click(screen.getByRole("button", { name: /Generate story plan/ }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Ollama is unavailable");
    await waitFor(() => expect(screen.getByRole("button", { name: /Generate story plan/ })).toBeEnabled());
  });
});

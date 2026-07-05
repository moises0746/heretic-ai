import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Dashboard from "./page";

describe("Dashboard", () => {
  it("presents the local studio and working video entry point", () => {
    render(<Dashboard />);

    expect(screen.getByRole("heading", { name: "Your creative pipeline, under your control." })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Create a video/ })).toHaveAttribute("href", "/create");
    expect(screen.getByRole("heading", { name: "Video Studio" })).toBeInTheDocument();
    expect(screen.getAllByText("Ready")).toHaveLength(2);
  });

  it("labels roadmap capabilities without implying they are complete", () => {
    render(<Dashboard />);

    expect(screen.getByRole("heading", { name: "Asset Library" })).toBeInTheDocument();
    expect(screen.getByText("Phase 6")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Character Studio" })).toBeInTheDocument();
    expect(screen.getByText("Phase 7")).toBeInTheDocument();
  });
});

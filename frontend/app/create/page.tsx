import type { Metadata } from "next";
import CreateWorkspace from "../create-workspace";

export const metadata: Metadata = { title: "Create video" };
export default function CreatePage() { return <CreateWorkspace />; }

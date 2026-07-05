import type { Metadata } from "next";
import StudioSection from "../studio-section";
export const metadata: Metadata = { title: "Assets" };
export default function AssetsPage() { return <StudioSection eyebrow="PHASE 6" title="Asset Library" description="A reusable local library for every source file and generated output in your production workflow." status="Planned next" tone="setup" items={[{title:"Drag and drop",description:"Upload images, audio, video, documents, and reference material with progress feedback."},{title:"Safe local storage",description:"Validate formats and filenames while keeping originals under your control."},{title:"Search and reuse",description:"Add metadata, previews, filtering, and project links without duplicating assets."}]} />; }

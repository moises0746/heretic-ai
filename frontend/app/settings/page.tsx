import type { Metadata } from "next";
import StudioSection from "../studio-section";
export const metadata: Metadata = { title: "Settings" };
export default function SettingsPage() { return <StudioSection eyebrow="SETTINGS" title="Local runtime configuration" description="Runtime values currently stay in environment files so credentials and machine-specific paths never enter source control." status="Environment managed" tone="setup" items={[{title:"Model providers",description:"Configure Ollama, TTS, and image providers through backend environment variables."},{title:"Storage paths",description:"Keep generated assets and caches in explicit local directories."},{title:"Deployment",description:"Use the documented Docker Compose stack for repeatable self-hosting."}]} />; }

import type { Metadata } from "next";
import StudioSection from "../studio-section";
export const metadata: Metadata = { title: "Characters" };
export default function CharactersPage() { return <StudioSection eyebrow="PHASE 7" title="Character & Storyboard Studio" description="Turn reference sheets and storyboard panels into consistent, shot-aware generation instructions." status="Roadmap" items={[{title:"Character references",description:"Connect approved turnarounds, expressions, outfits, and color palettes."},{title:"Storyboard planning",description:"Map uploaded panels to scenes, timings, dialogue, camera, and motion."},{title:"Continuity controls",description:"Carry identity and visual rules across every generated scene."}]} />; }

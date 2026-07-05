import Link from "next/link";

const studios = [
  {
    title: "Video Studio",
    description: "Generate scripts, narration, scene images, subtitles, and local MP4 files.",
    status: "Ready",
    tone: "ready",
    href: "/create",
    action: "Open studio",
    icon: "play",
  },
  {
    title: "Image Studio",
    description: "Create deterministic 16:9 scene art with a configured FLUX provider.",
    status: "Setup required",
    tone: "setup",
    href: "/create",
    action: "Use in video flow",
    icon: "image",
  },
  {
    title: "Voice Studio",
    description: "Save reference voices and synthesize narration through the local TTS pipeline.",
    status: "Ready",
    tone: "ready",
    href: "/voices",
    action: "Manage voices",
    icon: "wave",
  },
  {
    title: "Asset Library",
    description: "Drag, drop, organize, and reuse images, audio, video, and source material.",
    status: "Phase 6",
    tone: "planned",
    href: "/assets",
    action: "View roadmap",
    icon: "folder",
  },
  {
    title: "Character Studio",
    description: "Keep characters visually consistent across reference sheets and storyboards.",
    status: "Phase 7",
    tone: "planned",
    href: "/characters",
    action: "View roadmap",
    icon: "character",
  },
  {
    title: "Podcast & Marketing",
    description: "Long-form audio, social clips, ads, and reusable brand workflows.",
    status: "Vision",
    tone: "planned",
    href: "/projects",
    action: "Explore direction",
    icon: "spark",
  },
];

const workflow = ["Idea", "Story plan", "Voice", "Images", "Video", "Export"];

function StudioIcon({ name }: { name: string }) {
  const paths: Record<string, React.ReactNode> = {
    play: <><path d="M6 4.8a2 2 0 0 1 3-1.72l9.8 5.7a2 2 0 0 1 0 3.44L9 17.92A2 2 0 0 1 6 16.2Z" /><path d="M18 5.5 20 4m-2 14.5 2 1.5" /></>,
    image: <><rect x="3" y="4" width="18" height="16" rx="2" /><circle cx="8.5" cy="9" r="1.5" /><path d="m4 17 5-5 4 4 2-2 5 4" /></>,
    wave: <><path d="M4 10v4m4-7v10m4-14v18m4-14v10m4-7v4" /></>,
    folder: <><path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" /></>,
    character: <><circle cx="12" cy="8" r="4" /><path d="M5 21a7 7 0 0 1 14 0" /><path d="M18.5 4.5 20 3m-2 6 2 1" /></>,
    spark: <><path d="m12 3 1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5Z" /><path d="m19 15 .7 2.3L22 18l-2.3.7L19 21l-.7-2.3L16 18l2.3-.7Z" /></>,
  };

  return <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div className="hero-copy">
          <p className="eyebrow">LOCAL-FIRST CREATIVE STUDIO</p>
          <h1>Your creative pipeline, under your control.</h1>
          <p className="subtitle">
            Build videos with private AI models, local storage, and a workflow you can inspect from idea to export.
          </p>
          <div className="hero-actions">
            <Link className="button primary-button" href="/create">Create a video <span aria-hidden="true">→</span></Link>
            <Link className="button secondary-button" href="/assets">Plan your assets</Link>
          </div>
        </div>
        <div className="hero-orbit" aria-hidden="true">
          <div className="orbit-ring orbit-ring-one" />
          <div className="orbit-ring orbit-ring-two" />
          <div className="orbit-core"><span>H</span></div>
          <span className="orbit-node node-one" />
          <span className="orbit-node node-two" />
          <span className="orbit-node node-three" />
        </div>
      </section>

      <section className="workflow-card" aria-labelledby="workflow-heading">
        <div>
          <p className="section-kicker">WORKFLOW ENGINE</p>
          <h2 id="workflow-heading">One connected production path</h2>
        </div>
        <ol className="workflow-steps">
          {workflow.map((step, index) => (
            <li key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{step}</strong>
            </li>
          ))}
        </ol>
      </section>

      <section className="dashboard-section" aria-labelledby="studios-heading">
        <div className="section-heading">
          <div>
            <p className="section-kicker">CREATIVE TOOLS</p>
            <h2 id="studios-heading">Choose a studio</h2>
          </div>
          <p>Capabilities are labeled by their actual implementation status.</p>
        </div>
        <div className="studio-grid">
          {studios.map((studio) => (
            <article className="studio-card" key={studio.title}>
              <div className="studio-card-top">
                <span className="studio-icon"><StudioIcon name={studio.icon} /></span>
                <span className={`status-badge ${studio.tone}`}>{studio.status}</span>
              </div>
              <div>
                <h3>{studio.title}</h3>
                <p>{studio.description}</p>
              </div>
              <Link href={studio.href}>{studio.action} <span aria-hidden="true">↗</span></Link>
            </article>
          ))}
        </div>
      </section>

      <div className="dashboard-columns">
        <section className="dashboard-panel" aria-labelledby="readiness-heading">
          <p className="section-kicker">SYSTEM READINESS</p>
          <h2 id="readiness-heading">What works today</h2>
          <ul className="readiness-list">
            <li><span className="readiness-dot ready" /><div><strong>Script generation</strong><small>Ollama + Qwen integration</small></div><span>Implemented</span></li>
            <li><span className="readiness-dot ready" /><div><strong>Voice and video pipeline</strong><small>Queued local jobs</small></div><span>Implemented</span></li>
            <li><span className="readiness-dot setup" /><div><strong>Image generation</strong><small>Requires a configured accelerator</small></div><span>Configure</span></li>
            <li><span className="readiness-dot planned" /><div><strong>Authentication</strong><small>Required before shared projects</small></div><span>Pending</span></li>
          </ul>
        </section>
        <section className="dashboard-panel roadmap-panel" aria-labelledby="roadmap-heading">
          <p className="section-kicker">NEXT MILESTONE</p>
          <h2 id="roadmap-heading">Build the Asset Library</h2>
          <p>Phase 6 adds the reusable material layer: drag-and-drop uploads, metadata, previews, and safe local file storage.</p>
          <div className="phase-track" aria-label="Roadmap: core pipeline built, platform foundation active, asset library next, character studio later">
            <span className="built">Core pipeline</span>
            <span className="active">Platform</span>
            <span className="next">Assets next</span>
            <span>Characters</span>
          </div>
          <Link href="/assets">See the planned scope →</Link>
        </section>
      </div>
    </div>
  );
}

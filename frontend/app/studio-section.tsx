import Link from "next/link";

type StudioSectionProps = {
  eyebrow: string;
  title: string;
  description: string;
  status: string;
  tone?: "ready" | "setup" | "planned";
  items: { title: string; description: string }[];
  action?: { href: string; label: string };
};

export default function StudioSection({ eyebrow, title, description, status, tone = "planned", items, action }: StudioSectionProps) {
  return (
    <div className="section-page">
      <header className="workspace-heading section-page-heading">
        <div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{description}</p></div>
        <span className={`status-badge ${tone}`}>{status}</span>
      </header>
      <section className="scope-panel">
        <div className="scope-heading"><p className="section-kicker">CURRENT SCOPE</p><h2>Designed for the local workflow</h2></div>
        <div className="scope-grid">
          {items.map((item, index) => <article key={item.title}><span>{String(index + 1).padStart(2, "0")}</span><h3>{item.title}</h3><p>{item.description}</p></article>)}
        </div>
        {action && <Link className="button primary-button scope-action" href={action.href}>{action.label} <span aria-hidden="true">→</span></Link>}
      </section>
    </div>
  );
}

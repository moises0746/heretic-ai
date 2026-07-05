"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navigation = [
  { href: "/", label: "Dashboard", icon: "grid" },
  { href: "/create", label: "Create", icon: "plus" },
  { href: "/projects", label: "Projects", icon: "layers" },
  { href: "/assets", label: "Assets", icon: "folder" },
  { href: "/characters", label: "Characters", icon: "user" },
  { href: "/voices", label: "Voices", icon: "wave" },
  { href: "/jobs", label: "Jobs", icon: "activity" },
  { href: "/settings", label: "Settings", icon: "settings" },
];

function NavIcon({ name }: { name: string }) {
  const paths: Record<string, React.ReactNode> = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" /></>,
    plus: <><path d="M12 5v14M5 12h14" /><circle cx="12" cy="12" r="9" /></>,
    layers: <><path d="m12 3 9 5-9 5-9-5Z" /><path d="m3 12 9 5 9-5M3 16l9 5 9-5" /></>,
    folder: <path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" />,
    user: <><circle cx="12" cy="8" r="4" /><path d="M5 21a7 7 0 0 1 14 0" /></>,
    wave: <path d="M4 10v4m4-7v10m4-14v18m4-14v10m4-7v4" />,
    activity: <path d="M3 12h4l2-7 4 14 2-7h6" />,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.83 2.83-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .6 1.7 1.7 0 0 0-.4 1.1V21h-4v-.09A1.7 1.7 0 0 0 8.6 19.4a1.7 1.7 0 0 0-1.88.34l-.06.06-2.83-2.83.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.6-1 1.7 1.7 0 0 0-1.1-.4H3v-4h.09A1.7 1.7 0 0 0 4.6 8.6a1.7 1.7 0 0 0-.34-1.88l-.06-.06 2.83-2.83.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.6 1.7 1.7 0 0 0 .4-1.1V3h4v.09A1.7 1.7 0 0 0 15.4 4.6a1.7 1.7 0 0 0 1.88-.34l.06-.06 2.83 2.83-.06.06A1.7 1.7 0 0 0 19.4 9c.1.37.31.71.6 1 .31.28.7.42 1.1.4h.1v4h-.1A1.7 1.7 0 0 0 19.4 15Z" /></>,
  };
  return <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

export default function StudioShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const current = navigation.find((item) => item.href === pathname)?.label ?? "Studio";

  return (
    <div className="app-shell">
      <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
        <Link className="shell-brand" href="/" onClick={() => setMenuOpen(false)}>
          <Image src="/heretic-mark.svg" alt="" width={38} height={38} priority />
          <span><strong>Heretic</strong><small>AI Studio</small></span>
        </Link>
        <nav aria-label="Main navigation">
          {navigation.map((item, index) => (
            <Link
              className={`${pathname === item.href ? "active" : ""} ${index === 7 ? "settings-link" : ""}`}
              href={item.href}
              key={item.href}
              onClick={() => setMenuOpen(false)}
            >
              <NavIcon name={item.icon} />
              <span>{item.label}</span>
              {item.href === "/assets" && <small>Next</small>}
            </Link>
          ))}
        </nav>
        <div className="local-card">
          <span className="local-indicator" />
          <div><strong>Local workspace</strong><small>Private by default</small></div>
        </div>
      </aside>
      {menuOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
      <div className="shell-main">
        <header className="topbar">
          <button className="menu-button" aria-label="Open navigation" onClick={() => setMenuOpen(true)}>
            <span /><span /><span />
          </button>
          <div><p>Workspace</p><strong>{current}</strong></div>
          <span className="privacy-pill"><span /> Runs locally</span>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  );
}

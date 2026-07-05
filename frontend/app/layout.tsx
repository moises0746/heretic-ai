import type { Metadata } from "next";
import "./globals.css";
import StudioShell from "./studio-shell";

export const metadata: Metadata = {
  title: {
    default: "Heretic AI Studio",
    template: "%s | Heretic AI Studio",
  },
  description: "A private, self-hosted AI creative studio for local video production.",
  icons: {
    icon: "/heretic-mark.svg",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body><StudioShell>{children}</StudioShell></body>
    </html>
  );
}


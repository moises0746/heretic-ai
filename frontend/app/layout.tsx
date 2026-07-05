import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Heretic AI",
  description: "Self-hosted AI video generation",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}


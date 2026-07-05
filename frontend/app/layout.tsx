import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Heretic",
  description: "Self-hosted AI video generation",
  icons: {
    icon: "/heretic-mark.svg",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}


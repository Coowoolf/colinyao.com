"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

/** nav = 纯四维：时 空 内 外；字标「同一把尺子」= 合上 → 进书 */
const links = [
  { href: "/time", label: "时", match: /^\/time/ },
  { href: "/space", label: "空", match: /^\/space/ },
  { href: "/inward", label: "内", match: /^\/inward/ },
  { href: "/outward", label: "外", match: /^\/outward/ },
];

export default function Nav() {
  const pathname = usePathname();
  const [theme, setTheme] = useState<"dark" | "light" | null>(null);

  useEffect(() => {
    setTheme(document.documentElement.dataset.theme === "light" ? "light" : "dark");
  }, []);

  const toggle = () => {
    const next = theme === "light" ? "dark" : "light";
    if (next === "light") document.documentElement.dataset.theme = "light";
    else delete document.documentElement.dataset.theme;
    try {
      localStorage.setItem("colin-theme", next);
    } catch {}
    setTheme(next);
  };

  return (
    <nav className="nav">
      <div className="nav-inner">
        <Link href="/" className="nav-mark" aria-label="回到主页">
          COLIN<span className="tick">·</span>YAO
        </Link>
        <div className="nav-links" style={{ alignItems: "center" }}>
          {links.map((l) => (
            <Link key={l.href} href={l.href} className={l.match.test(pathname) ? "active" : ""}>
              {l.label}
            </Link>
          ))}
          <button
            className="theme-toggle"
            onClick={toggle}
            aria-label="切换深浅主题"
            suppressHydrationWarning
          >
            {theme === null ? "·" : theme === "dark" ? "浅底" : "暗底"}
          </button>
        </div>
      </div>
    </nav>
  );
}

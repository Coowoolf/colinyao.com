"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/talks", label: "TALKS" },
  { href: "/ideas", label: "IDEAS" },
  { href: "/about", label: "ABOUT" },
];

export default function Nav() {
  const pathname = usePathname();
  return (
    <nav className="nav">
      <div className="nav-inner">
        <Link href="/" className="nav-mark" aria-label="首页">
          COLIN<span className="tick">·</span>YAO
        </Link>
        <div className="nav-links">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className={pathname.startsWith(l.href) ? "active" : ""}>
              {l.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

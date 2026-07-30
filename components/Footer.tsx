import { site } from "@/content/site";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="sig">
          © 2026 COLIN YAO 姚光华
          <br />
          <span className="co">同一把尺子</span>，向外叫 EVAL，向内叫内观。
        </div>
        <div className="footer-links">
          {site.links.map((l) =>
            l.href ? (
              <a key={l.name} href={l.href} target={l.href.startsWith("http") ? "_blank" : undefined} rel="noreferrer">
                {l.name} · {l.value}
              </a>
            ) : (
              <span key={l.name} className="footer-plain">
                {l.name} · {l.value}
              </span>
            )
          )}
        </div>
      </div>
    </footer>
  );
}

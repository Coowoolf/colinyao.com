import { site } from "@/content/site";
import { book } from "@/content/book";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="sig">
          《{book.title}》· {book.author} 著
          <br />
          <span className="co">向外叫 EVAL</span>，向内叫内观。
          <br />
          <span className="colophon">{book.edition} · © 2026 COLINYAO.COM</span>
        </div>
        <div className="footer-links">
          <span className="footer-plain">
            {site.links.map((l) => l.name).join(" / ")} · {site.links[0].value}
          </span>
        </div>
      </div>
    </footer>
  );
}

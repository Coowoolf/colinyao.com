import type { MetadataRoute } from "next";
import { site } from "@/content/site";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["", "/time", "/space", "/inward", "/outward", "/preface", "/vol1", "/vol2", "/vol3", "/vol4", "/vol5"].map((p) => ({
    url: `${site.url}${p}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: p === "" ? 1 : 0.8,
  }));
}

import type { Metadata } from "next";
import DimensionPage from "@/components/DimensionPage";
import { rays } from "@/content/ruler";

const ray = rays.find((r) => r.id === "space")!;
export const metadata: Metadata = {
  title: `空 · ${ray.name}`,
  description: ray.intro,
};

export default function Page() {
  return <DimensionPage id="space" />;
}

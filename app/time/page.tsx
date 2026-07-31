import type { Metadata } from "next";
import DimensionPage from "@/components/DimensionPage";
import { rays } from "@/content/ruler";

const ray = rays.find((r) => r.id === "time")!;
export const metadata: Metadata = {
  title: `时 · ${ray.name}`,
  description: ray.intro,
};

export default function Page() {
  return <DimensionPage id="time" />;
}

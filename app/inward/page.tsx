import type { Metadata } from "next";
import DimensionPage from "@/components/DimensionPage";
import { rays } from "@/content/ruler";

const ray = rays.find((r) => r.id === "inw")!;
export const metadata: Metadata = {
  title: `内 · ${ray.name}`,
  description: ray.intro,
};

export default function Page() {
  return <DimensionPage id="inw" />;
}

import type { Metadata } from "next";
import VolumePage from "@/components/VolumePage";
import { volumes } from "@/content/book";

const v = volumes[0];
export const metadata: Metadata = {
  title: `卷一 · ${v.zh}`,
  description: v.intro.slice(0, 80),
};

export default function Page() {
  return <VolumePage no={1} />;
}

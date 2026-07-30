import type { Metadata } from "next";
import VolumePage from "@/components/VolumePage";
import { volumes } from "@/content/book";

const v = volumes[2];
export const metadata: Metadata = {
  title: `卷三 · ${v.zh}`,
  description: v.intro.slice(0, 80),
};

export default function Page() {
  return <VolumePage no={3} />;
}

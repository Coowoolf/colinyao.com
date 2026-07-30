/** 舞台底流场 —— 全站一直在走的暗流（源自 colin-deck-dark reference/flow-field.svg） */
export default function FlowField() {
  return (
    <>
      <svg
        className="site-flow"
        viewBox="0 0 1920 1080"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <g>
          <path className="l1 s1" strokeWidth="1.6" d="M-200 250 C 260 120, 520 400, 900 260 S 1560 90, 2120 240" />
          <path className="l2 s2" strokeWidth="1.2" d="M-200 340 C 300 220, 620 500, 980 350 S 1600 200, 2120 330" />
          <path className="l2 s3" strokeWidth="1" d="M-200 160 C 340 60, 700 300, 1060 150 S 1660 20, 2120 140" />
        </g>
        <g>
          <path className="l1 s2" strokeWidth="1.4" d="M-200 700 C 300 580, 640 860, 1020 720 S 1640 560, 2120 690" />
          <path className="l2 s4" strokeWidth="1.1" d="M-200 800 C 260 700, 600 960, 1000 820 S 1620 670, 2120 790" />
          <path className="l2 s1" strokeWidth="1" d="M-200 610 C 380 500, 720 780, 1100 620 S 1700 470, 2120 600" />
        </g>
        <g>
          <path className="l2 s3" strokeWidth=".9" d="M-200 980 C 320 880, 680 1120, 1080 980 S 1680 840, 2120 960" />
          <path className="l1 s4" strokeWidth="1.1" d="M-200 470 C 340 380, 660 640, 1040 500 S 1660 360, 2120 470" />
        </g>
      </svg>
      <div className="grid-veil" aria-hidden="true" />
    </>
  );
}

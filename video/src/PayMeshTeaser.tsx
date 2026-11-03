import React from "react";
import { Sequence } from "remotion";
import { IntroScene } from "./scenes/IntroScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { ShowcaseScene } from "./scenes/ShowcaseScene";
import { OutroScene } from "./scenes/OutroScene";

export const PayMeshTeaser: React.FC = () => {
  return (
    <div style={{ flex: 1, display: "flex", width: "100%", height: "100%" }}>
      {/* Scene 1: Quick Intro (3s) */}
      <Sequence from={0} durationInFrames={90}>
        <IntroScene />
      </Sequence>

      {/* Scene 2: Solution Core (4s) */}
      <Sequence from={90} durationInFrames={120}>
        <SolutionScene />
      </Sequence>

      {/* Scene 3: Platform Showcase (5s) */}
      <Sequence from={210} durationInFrames={150}>
        <ShowcaseScene />
      </Sequence>

      {/* Scene 4: Outro (3s) */}
      <Sequence from={360} durationInFrames={90}>
        <OutroScene />
      </Sequence>
    </div>
  );
};

import React from "react";
import { Sequence } from "remotion";
import { IntroScene } from "./scenes/IntroScene";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { ShowcaseScene } from "./scenes/ShowcaseScene";
import { ArchitectureScene } from "./scenes/ArchitectureScene";
import { OutroScene } from "./scenes/OutroScene";

export const PayMeshDemo: React.FC = () => {
  return (
    <div style={{ flex: 1, display: "flex", width: "100%", height: "100%" }}>
      {/* Scene 1: Kinetic Intro */}
      <Sequence from={0} durationInFrames={150}>
        <IntroScene />
      </Sequence>

      {/* Scene 2: The Bottleneck */}
      <Sequence from={150} durationInFrames={210}>
        <ProblemScene />
      </Sequence>

      {/* Scene 3: The PayMesh Solution */}
      <Sequence from={360} durationInFrames={240}>
        <SolutionScene />
      </Sequence>

      {/* Scene 4: 7-Screenshot UI Walkthrough */}
      <Sequence from={600} durationInFrames={840}>
        <ShowcaseScene />
      </Sequence>

      {/* Scene 5: Architecture & Security */}
      <Sequence from={1440} durationInFrames={210}>
        <ArchitectureScene />
      </Sequence>

      {/* Scene 6: Outro & Summary */}
      <Sequence from={1650} durationInFrames={150}>
        <OutroScene />
      </Sequence>
    </div>
  );
};


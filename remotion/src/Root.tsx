import React from "react";
import { Composition } from "remotion";
import { PayMeshDemo } from "./PayMeshDemo";
import { PayMeshTeaser } from "./PayMeshTeaser";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PayMeshDemo"
        component={PayMeshDemo}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="PayMeshTeaser"
        component={PayMeshTeaser}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { NeoCard } from "../components/NeoCard";
import { HeaderBadge } from "../components/HeaderBadge";

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titlePop = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.8 },
  });

  const subtitleOpacity = interpolate(frame, [25, 45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const badgeSlide = interpolate(frame, [10, 35], [-50, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#f8fafc",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px",
        fontFamily: "Inter, system-ui, -apple-system, sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Decorative Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "linear-gradient(to right, #e2e8f0 1px, transparent 1px), linear-gradient(to bottom, #e2e8f0 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          opacity: 0.6,
        }}
      />

      {/* Header Pill */}
      <div
        style={{
          transform: `translateY(${badgeSlide}px)`,
          opacity: subtitleOpacity,
          marginBottom: "36px",
          zIndex: 10,
        }}
      >
        <HeaderBadge label="PayPal AI Hackathon 2026" sublabel="Live Product Demo" />
      </div>

      {/* Hero Card */}
      <div
        style={{
          transform: `scale(${titlePop})`,
          zIndex: 10,
          maxWidth: "1100px",
          width: "100%",
        }}
      >
        <NeoCard bg="#ffffff" shadowColor="#0f172a">
          <div style={{ textAlign: "center", padding: "30px 20px" }}>
            <div
              style={{
                display: "inline-block",
                backgroundColor: "#0284c7",
                color: "#ffffff",
                padding: "6px 14px",
                borderRadius: "6px",
                fontSize: "16px",
                fontWeight: 700,
                fontFamily: "monospace",
                marginBottom: "20px",
                border: "2px solid #0f172a",
              }}
            >
              AUTONOMOUS COMMERCE INFRASTRUCTURE
            </div>

            <h1
              style={{
                fontSize: "76px",
                fontWeight: 900,
                color: "#0f172a",
                margin: "0 0 20px 0",
                letterSpacing: "-2px",
                lineHeight: 1.05,
              }}
            >
              PayMesh <span style={{ color: "#0284c7" }}>AI</span>
            </h1>

            <p
              style={{
                fontSize: "28px",
                color: "#475569",
                fontWeight: 600,
                margin: "0 0 32px 0",
              }}
            >
              A Trust & Payment Infrastructure for Autonomous AI Commerce
            </p>

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: "20px",
                opacity: subtitleOpacity,
              }}
            >
              <div
                style={{
                  backgroundColor: "#fef9c3",
                  border: "2px solid #0f172a",
                  borderRadius: "8px",
                  padding: "10px 20px",
                  fontSize: "18px",
                  fontWeight: 700,
                  fontFamily: "monospace",
                  color: "#854d0e",
                }}
              >
                ⚡ HTTP 402 / L402 Engine
              </div>
              <div
                style={{
                  backgroundColor: "#e0f2fe",
                  border: "2px solid #0f172a",
                  borderRadius: "8px",
                  padding: "10px 20px",
                  fontSize: "18px",
                  fontWeight: 700,
                  fontFamily: "monospace",
                  color: "#0369a1",
                }}
              >
                💳 PayPal Vault v3 Non-Custodial
              </div>
              <div
                style={{
                  backgroundColor: "#dcfce7",
                  border: "2px solid #0f172a",
                  borderRadius: "8px",
                  padding: "10px 20px",
                  fontSize: "18px",
                  fontWeight: 700,
                  fontFamily: "monospace",
                  color: "#15803d",
                }}
              >
                🛡️ Non-Custodial Policy Limits
              </div>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  );
};

import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { SlideInfo } from "../types";
import { HeaderBadge } from "../components/HeaderBadge";

const slides: SlideInfo[] = [
  {
    title: "1. Agent Workspace & FinTech Modal",
    category: "AUTONOMOUS AGENT ORCHESTRATION",
    image: "screenshots/01-agent-workspace.png",
    description: "Real-time streaming terminal with human-in-the-loop authorization modal for high-value API queries.",
    badge: "AGENT STUDIO",
  },
  {
    title: "2. Cryptographic L402 Challenge Card",
    category: "HTTP 402 PROTOCOL NEGOTIATION",
    image: "screenshots/02-l402-challenge.png",
    description: "Detailed breakdown of challenge invoice, SHA-256 HMAC hash, merchant ID, and PayPal Sandbox endpoint.",
    badge: "L402 INSPECTOR",
  },
  {
    title: "3. Unlocked Intelligence & Telemetry",
    category: "INSTANT ACCESS & VALIDATION",
    image: "screenshots/03-unlocked-intelligence.png",
    description: "Sub-500ms data pipeline unlock with 100% cryptographic token verification and channel telemetry.",
    badge: "INTELLIGENCE UNLOCKED",
  },
  {
    title: "4. Policy & Risk Manager",
    category: "NON-CUSTODIAL SAFETY RAILS",
    image: "screenshots/04-spending-policy.png",
    description: "24-hour rolling budget utilization gauge, single-transaction spending caps, and domain whitelisting.",
    badge: "BUDGET GAUGE",
  },
  {
    title: "5. Marketplace Catalogue",
    category: "NEO-TECH SERVICE REGISTRY",
    image: "screenshots/05-marketplace-catalogue.png",
    description: "Dynamic pricing discovery, category filtering chips (All, Hardware, News), and verified merchant badges.",
    badge: "DISCOVERY MESH",
  },
  {
    title: "6. Immutable Financial Audit Ledger",
    category: "COMPLIANCE & SETTLEMENT",
    image: "screenshots/06-financial-ledger.png",
    description: "AG Grid high-density transaction ledger with one-click CSV export utility and Vault health status.",
    badge: "AUDIT LEDGER",
  },
  {
    title: "7. Merchant Publisher Console",
    category: "MONETIZE APIS & DATASETS",
    image: "screenshots/07-merchant-studio.png",
    description: "Dynamic URL auto-slug generation, custom pricing tiers, PayPal payout onboarding, and live catalogue links.",
    badge: "MERCHANT STUDIO",
  },
];

export const ShowcaseScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideDuration = 120; // 4 seconds per slide (7 slides = 840 frames)
  const currentSlideIndex = Math.min(
    Math.floor(frame / slideDuration),
    slides.length - 1
  );
  const slide = slides[currentSlideIndex];
  const slideFrame = frame % slideDuration;

  const imageZoom = interpolate(slideFrame, [0, slideDuration], [1, 1.04], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const slideFade = spring({
    frame: slideFrame,
    fps,
    config: { damping: 15 },
  });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#0f172a",
        display: "flex",
        flexDirection: "column",
        padding: "40px 60px",
        fontFamily: "Inter, system-ui, sans-serif",
        color: "#ffffff",
        position: "relative",
      }}
    >
      {/* Top Bar Navigation */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <HeaderBadge label="Live Platform Walkthrough" sublabel={`Slide ${currentSlideIndex + 1} of 7`} color="#38bdf8" />
        <div
          style={{
            fontFamily: "monospace",
            backgroundColor: "#1e293b",
            padding: "6px 14px",
            borderRadius: "6px",
            border: "1px solid #475569",
            color: "#facc15",
            fontWeight: "bold",
            fontSize: "14px",
          }}
        >
          {slide.category}
        </div>
      </div>

      {/* Main Showcase Grid */}
      <div
        style={{
          flex: 1,
          display: "grid",
          gridTemplateColumns: "1.3fr 0.7fr",
          gap: "30px",
          alignItems: "center",
        }}
      >
        {/* Screenshot Viewport */}
        <div
          style={{
            backgroundColor: "#1e293b",
            borderRadius: "14px",
            border: "4px solid #facc15",
            boxShadow: "8px 8px 0px #0284c7",
            overflow: "hidden",
            height: "640px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
            transform: `scale(${slideFade})`,
          }}
        >
          <Img
            src={staticFile(slide.image)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
              transform: `scale(${imageZoom})`,
            }}
          />
        </div>

        {/* Feature Explainer Card */}
        <div
          style={{
            backgroundColor: "#ffffff",
            color: "#0f172a",
            borderRadius: "14px",
            border: "3px solid #0f172a",
            boxShadow: "6px 6px 0px #facc15",
            padding: "36px",
            display: "flex",
            flexDirection: "column",
            gap: "20px",
          }}
        >
          <div
            style={{
              display: "inline-block",
              backgroundColor: "#fef08a",
              color: "#854d0e",
              border: "2px solid #0f172a",
              padding: "4px 12px",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: 800,
              fontFamily: "monospace",
              width: "fit-content",
            }}
          >
            {slide.badge}
          </div>

          <h3
            style={{
              fontSize: "36px",
              fontWeight: 900,
              margin: 0,
              color: "#0f172a",
              lineHeight: 1.2,
            }}
          >
            {slide.title}
          </h3>

          <p
            style={{
              fontSize: "20px",
              color: "#475569",
              lineHeight: 1.5,
              margin: 0,
            }}
          >
            {slide.description}
          </p>

          <div
            style={{
              marginTop: "16px",
              borderTop: "2px solid #e2e8f0",
              paddingTop: "20px",
              display: "flex",
              flexDirection: "column",
              gap: "10px",
              fontFamily: "monospace",
              fontSize: "15px",
            }}
          >
            <div style={{ color: "#0284c7", fontWeight: 700 }}>
              ✔ Verified via Automated Test Suite
            </div>
            <div style={{ color: "#16a34a", fontWeight: 700 }}>
              ✔ Responsive Neo-Tech Styling
            </div>
            <div style={{ color: "#64748b" }}>
              ⚡ 100% Working Sandbox Integration
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};


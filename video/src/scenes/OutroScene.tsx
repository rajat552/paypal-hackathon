import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { NeoCard } from "../components/NeoCard";
import { HeaderBadge } from "../components/HeaderBadge";

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 12 } });

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
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <div style={{ marginBottom: "28px" }}>
        <HeaderBadge label="Built for PayPal AI Hackathon 2026" color="#facc15" />
      </div>

      <div style={{ transform: `scale(${pop})`, maxWidth: "1000px", width: "100%" }}>
        <NeoCard bg="#ffffff" shadowColor="#0f172a">
          <div style={{ textAlign: "center", padding: "30px 20px" }}>
            <h2 style={{ fontSize: "64px", fontWeight: 900, color: "#0f172a", margin: "0 0 16px 0" }}>
              PayMesh <span style={{ color: "#0284c7" }}>AI</span>
            </h2>
            <p style={{ fontSize: "24px", color: "#475569", fontWeight: 600, margin: "0 0 32px 0" }}>
              Powering the Next Generation of Autonomous Agent Transactions.
            </p>

            <div
              style={{
                display: "inline-flex",
                flexDirection: "column",
                gap: "12px",
                backgroundColor: "#f1f5f9",
                border: "2px solid #0f172a",
                borderRadius: "10px",
                padding: "20px 40px",
                fontFamily: "monospace",
                fontSize: "18px",
                color: "#0f172a",
                boxShadow: "4px 4px 0px #0f172a",
              }}
            >
              <div><strong>GitHub:</strong> github.com/rajat552/paypal-hackathon</div>
              <div><strong>Stack:</strong> FastAPI • React • PayPal Vault v3 • L402 • MCP</div>
              <div><strong>Status:</strong> 100% Verified & Tested Sandbox Environment</div>
            </div>

            <div style={{ marginTop: "32px", fontSize: "18px", color: "#64748b", fontWeight: 500 }}>
              Thank You! Ready for Judges & Live Demonstration.
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  );
};

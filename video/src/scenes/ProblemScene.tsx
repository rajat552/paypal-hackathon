import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { NeoCard } from "../components/NeoCard";
import { HeaderBadge } from "../components/HeaderBadge";

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardEntrance = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  const alertBlink = Math.sin(frame * 0.3) > 0 ? 1 : 0.8;

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#fff1f2",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px",
        fontFamily: "Inter, system-ui, sans-serif",
        position: "relative",
      }}
    >
      <div style={{ marginBottom: "24px", zIndex: 10 }}>
        <HeaderBadge label="The Core Bottleneck" sublabel="AI Commerce in 2026" color="#fca5a5" />
      </div>

      <div
        style={{
          transform: `scale(${cardEntrance})`,
          maxWidth: "1150px",
          width: "100%",
          zIndex: 10,
        }}
      >
        <NeoCard bg="#ffffff" borderColor="#e11d48" shadowColor="#881337">
          <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: "32px", alignItems: "center" }}>
            <div>
              <div
                style={{
                  display: "inline-block",
                  backgroundColor: "#ffe4e6",
                  color: "#be123c",
                  padding: "4px 12px",
                  borderRadius: "6px",
                  fontSize: "15px",
                  fontWeight: 700,
                  fontFamily: "monospace",
                  marginBottom: "12px",
                  border: "2px solid #e11d48",
                }}
              >
                THE PROBLEM
              </div>
              <h2
                style={{
                  fontSize: "44px",
                  fontWeight: 900,
                  color: "#0f172a",
                  lineHeight: 1.15,
                  margin: "0 0 16px 0",
                }}
              >
                AI Agents Cannot Autonomously Pay for Web Data.
              </h2>
              <p style={{ fontSize: "20px", color: "#475569", lineHeight: 1.5, margin: "0 0 20px 0" }}>
                Autonomous LLM agents crawl APIs, premium datasets, and compute nodes—only to be halted dead in their tracks by paywalls requiring manual credit card entry.
              </p>

              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", fontSize: "17px", fontWeight: 600, color: "#be123c" }}>
                  <span>❌</span> No credit cards for autonomous bots (fraud & compliance risk)
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", fontSize: "17px", fontWeight: 600, color: "#be123c" }}>
                  <span>❌</span> Friction-heavy human-in-the-loop approvals break real-time workflows
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", fontSize: "17px", fontWeight: 600, color: "#be123c" }}>
                  <span>❌</span> Risk of rogue agent infinite loops draining organizational accounts
                </div>
              </div>
            </div>

            {/* Simulated Error Terminal */}
            <div
              style={{
                backgroundColor: "#0f172a",
                borderRadius: "10px",
                border: "2px solid #334155",
                boxShadow: "4px 4px 0px #020617",
                padding: "20px",
                fontFamily: "monospace",
                color: "#e2e8f0",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "14px", borderBottom: "1px solid #1e293b", paddingBottom: "10px" }}>
                <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#ef4444" }} />
                <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#eab308" }} />
                <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#22c55e" }} />
                <span style={{ fontSize: "13px", color: "#94a3b8", marginLeft: "10px" }}>agent-stdout — execution blocked</span>
              </div>

              <div style={{ fontSize: "14px", lineHeight: 1.6 }}>
                <div style={{ color: "#38bdf8" }}>&gt; GET /api/v1/protected/intel/channel3</div>
                <div style={{ color: "#94a3b8" }}>&gt; Host: api.merchants.mesh</div>
                <div style={{ color: "#94a3b8" }}>&gt; User-Agent: AutonomousAgent-v2</div>
                <div style={{ marginTop: "12px", padding: "10px", backgroundColor: "#3b0764", border: "1px solid #7e22ce", borderRadius: "6px" }}>
                  <span style={{ color: "#f43f5e", fontWeight: "bold", opacity: alertBlink }}>HTTP/1.1 402 PAYMENT REQUIRED</span>
                  <div style={{ color: "#e2e8f0", fontSize: "12px", marginTop: "4px" }}>
                    WWW-Authenticate: L402 invoice="INV-7841", macaroons="SHA256..."
                  </div>
                </div>
                <div style={{ marginTop: "12px", color: "#f87171" }}>
                  [FATAL] Agent halted. No custodial credentials available.
                </div>
              </div>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  );
};

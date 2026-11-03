import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { NeoCard } from "../components/NeoCard";
import { HeaderBadge } from "../components/HeaderBadge";

export const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 13 } });

  const step1Highlight = frame > 15 ? "#0284c7" : "#cbd5e1";
  const step2Highlight = frame > 45 ? "#16a34a" : "#cbd5e1";
  const step3Highlight = frame > 75 ? "#f59e0b" : "#cbd5e1";

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#f0fdf4",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <div style={{ marginBottom: "24px" }}>
        <HeaderBadge label="The PayMesh Solution" sublabel="Zero-Friction Autonomous Commerce" color="#86efac" />
      </div>

      <div style={{ transform: `scale(${pop})`, maxWidth: "1200px", width: "100%" }}>
        <NeoCard bg="#ffffff" borderColor="#16a34a" shadowColor="#14532d">
          <div style={{ textAlign: "center", marginBottom: "28px" }}>
            <h2 style={{ fontSize: "46px", fontWeight: 900, color: "#0f172a", margin: "0 0 10px 0" }}>
              The L402 + PayPal Trust Mesh
            </h2>
            <p style={{ fontSize: "20px", color: "#475569", margin: 0 }}>
              Autonomous protocol negotiation, cryptographic HMAC tokens, and automated PayPal Sandbox settlement.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "20px" }}>
            {/* Step 1 */}
            <div
              style={{
                backgroundColor: "#f8fafc",
                border: `3px solid ${step1Highlight}`,
                borderRadius: "10px",
                padding: "20px",
                boxShadow: "4px 4px 0px #0f172a",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <span style={{ backgroundColor: "#0284c7", color: "#fff", width: "28px", height: "28px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" }}>
                  1
                </span>
                <span style={{ fontFamily: "monospace", fontWeight: "bold", fontSize: "16px", color: "#0f172a" }}>
                  L402 Challenge
                </span>
              </div>
              <p style={{ fontSize: "15px", color: "#475569", lineHeight: 1.5 }}>
                Protected API returns HTTP 402 with price ($0.50 USD), invoice ID, and cryptographic challenge hash.
              </p>
            </div>

            {/* Step 2 */}
            <div
              style={{
                backgroundColor: "#f8fafc",
                border: `3px solid ${step2Highlight}`,
                borderRadius: "10px",
                padding: "20px",
                boxShadow: "4px 4px 0px #0f172a",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <span style={{ backgroundColor: "#16a34a", color: "#fff", width: "28px", height: "28px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" }}>
                  2
                </span>
                <span style={{ fontFamily: "monospace", fontWeight: "bold", fontSize: "16px", color: "#0f172a" }}>
                  Policy & PayPal Vault
                </span>
              </div>
              <p style={{ fontSize: "15px", color: "#475569", lineHeight: 1.5 }}>
                PayMesh checks agent daily spending budget ($50.00 max, 24h rolling limit) and triggers PayPal Vault v3 non-custodial capture.
              </p>
            </div>

            {/* Step 3 */}
            <div
              style={{
                backgroundColor: "#f8fafc",
                border: `3px solid ${step3Highlight}`,
                borderRadius: "10px",
                padding: "20px",
                boxShadow: "4px 4px 0px #0f172a",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
                <span style={{ backgroundColor: "#f59e0b", color: "#fff", width: "28px", height: "28px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" }}>
                  3
                </span>
                <span style={{ fontFamily: "monospace", fontWeight: "bold", fontSize: "16px", color: "#0f172a" }}>
                  Instant Unlock & Ledger
                </span>
              </div>
              <p style={{ fontSize: "15px", color: "#475569", lineHeight: 1.5 }}>
                Preimage token returned (&apos;L402 token:preimage&apos;). The resource unlocks in 0.48s and logs to the immutable financial ledger.
              </p>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  );
};

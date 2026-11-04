import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { NeoCard } from "../components/NeoCard";
import { HeaderBadge } from "../components/HeaderBadge";

export const ArchitectureScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14 } });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#f1f5f9",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <div style={{ marginBottom: "24px" }}>
        <HeaderBadge label="System Architecture & Trust Engine" sublabel="Built for Scale" color="#cbd5e1" />
      </div>

      <div style={{ transform: `scale(${entrance})`, maxWidth: "1200px", width: "100%" }}>
        <NeoCard bg="#ffffff" shadowColor="#0f172a">
          <div style={{ textAlign: "center", marginBottom: "32px" }}>
            <h2 style={{ fontSize: "44px", fontWeight: 900, color: "#0f172a", margin: "0 0 10px 0" }}>
              Enterprise-Grade FinTech & AI Integration
            </h2>
            <p style={{ fontSize: "20px", color: "#64748b", margin: 0 }}>
              Seamlessly bridging AI agents, protocol-level payments, and banking infrastructure.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
            {/* Box 1: PayPal Platform */}
            <div
              style={{
                backgroundColor: "#eff6ff",
                border: "2px solid #0284c7",
                borderRadius: "10px",
                padding: "24px",
                boxShadow: "4px 4px 0px #0369a1",
              }}
            >
              <div style={{ fontSize: "22px", fontWeight: 800, color: "#1e3a8a", marginBottom: "8px" }}>
                💳 PayPal Developer Platform
              </div>
              <ul style={{ fontSize: "16px", color: "#334155", lineHeight: 1.6, paddingLeft: "20px", margin: 0 }}>
                <li><strong>Vault v3 Integration:</strong> Non-custodial customer authorization tokens without bot card exposure.</li>
                <li><strong>Orders v2 & Sandbox Capture:</strong> Sub-second simulated and live payment settlement.</li>
                <li><strong>Webhook Verification:</strong> Cryptographic header validation and event reconciliation.</li>
              </ul>
            </div>

            {/* Box 2: L402 Engine */}
            <div
              style={{
                backgroundColor: "#fefce8",
                border: "2px solid #ca8a04",
                borderRadius: "10px",
                padding: "24px",
                boxShadow: "4px 4px 0px #854d0e",
              }}
            >
              <div style={{ fontSize: "22px", fontWeight: 800, color: "#713f12", marginBottom: "8px" }}>
                ⚡ L402 Cryptographic Protocol
              </div>
              <ul style={{ fontSize: "16px", color: "#334155", lineHeight: 1.6, paddingLeft: "20px", margin: 0 }}>
                <li><strong>SHA-256 HMAC Authentication:</strong> Tamper-proof token signatures and invoice hashes.</li>
                <li><strong>Preimage Generation:</strong> Unique access verification string generated upon capture.</li>
                <li><strong>Stateless Verification:</strong> High-throughput validation across edge microservices.</li>
              </ul>
            </div>

            {/* Box 3: Model Context Protocol (MCP) */}
            <div
              style={{
                backgroundColor: "#f0fdf4",
                border: "2px solid #16a34a",
                borderRadius: "10px",
                padding: "24px",
                boxShadow: "4px 4px 0px #14532d",
              }}
            >
              <div style={{ fontSize: "22px", fontWeight: 800, color: "#14532d", marginBottom: "8px" }}>
                🤖 Model Context Protocol (MCP)
              </div>
              <ul style={{ fontSize: "16px", color: "#334155", lineHeight: 1.6, paddingLeft: "20px", margin: 0 }}>
                <li><strong>Native Agent Tooling:</strong> LangChain & Claude Desktop tool specifications.</li>
                <li><strong>Tool Discovery:</strong> `paymesh_discover`, `paymesh_negotiate`, and `paymesh_settle`.</li>
                <li><strong>Autonomous Invocation:</strong> Agents autonomously check balances and capture tokens.</li>
              </ul>
            </div>

            {/* Box 4: Non-Custodial Policy Engine */}
            <div
              style={{
                backgroundColor: "#faf5ff",
                border: "2px solid #9333ea",
                borderRadius: "10px",
                padding: "24px",
                boxShadow: "4px 4px 0px #581c87",
              }}
            >
              <div style={{ fontSize: "22px", fontWeight: 800, color: "#581c87", marginBottom: "8px" }}>
                🛡️ Non-Custodial Policy Rails
              </div>
              <ul style={{ fontSize: "16px", color: "#334155", lineHeight: 1.6, paddingLeft: "20px", margin: 0 }}>
                <li><strong>Rolling 24-Hour Budgets:</strong> Automatic rate-limiting and budget cap enforcement.</li>
                <li><strong>Single-Transaction Caps:</strong> Hard stops preventing unauthorized high-value charges.</li>
                <li><strong>Domain Whitelisting:</strong> Strict merchant endpoint authorization tables.</li>
              </ul>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  );
};


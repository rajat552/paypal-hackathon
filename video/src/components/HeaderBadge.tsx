import React from "react";

interface HeaderBadgeProps {
  label: string;
  sublabel?: string;
  color?: string;
}

export const HeaderBadge: React.FC<HeaderBadgeProps> = ({
  label,
  sublabel,
  color = "#facc15",
}) => {
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "12px",
        backgroundColor: color,
        border: "2px solid #0f172a",
        boxShadow: "3px 3px 0px #0f172a",
        padding: "6px 16px",
        borderRadius: "8px",
        fontFamily: "monospace",
        fontWeight: "bold",
        fontSize: "18px",
        color: "#0f172a",
        textTransform: "uppercase",
        letterSpacing: "1px",
      }}
    >
      <span>●</span>
      <span>{label}</span>
      {sublabel && (
        <span
          style={{
            backgroundColor: "#0f172a",
            color: "#ffffff",
            padding: "2px 8px",
            borderRadius: "4px",
            fontSize: "14px",
          }}
        >
          {sublabel}
        </span>
      )}
    </div>
  );
};


import React from "react";

interface NeoCardProps {
  children: React.ReactNode;
  bg?: string;
  borderColor?: string;
  shadowColor?: string;
  style?: React.CSSProperties;
}

export const NeoCard: React.FC<NeoCardProps> = ({
  children,
  bg = "#ffffff",
  borderColor = "#0f172a",
  shadowColor = "#0f172a",
  style = {},
}) => {
  return (
    <div
      style={{
        backgroundColor: bg,
        border: `3px solid ${borderColor}`,
        boxShadow: `6px 6px 0px ${shadowColor}`,
        borderRadius: "12px",
        padding: "24px",
        ...style,
      }}
    >
      {children}
    </div>
  );
};


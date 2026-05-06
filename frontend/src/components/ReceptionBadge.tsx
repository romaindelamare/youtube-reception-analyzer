import { Chip } from "@mui/material";

interface ReceptionBadgeProps {
  label: "Positive" | "Mixed" | "Negative";
}

const CONFIG: Record<string, "success" | "warning" | "error"> = {
  Positive: "success",
  Mixed: "warning",
  Negative: "error",
};

export function ReceptionBadge({ label }: ReceptionBadgeProps) {
  const color = CONFIG[label] || "default";

  return (
    <Chip
      label={label}
      color={color as "success" | "warning" | "error"}
      variant="filled"
      sx={{ fontWeight: 600, fontSize: "0.95rem" }}
    />
  );
}

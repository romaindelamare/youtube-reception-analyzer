import { Box, LinearProgress, Typography, useTheme } from "@mui/material";
import type { SentimentBreakdown } from "../types/report";

interface SentimentBarsProps {
  sentiment: SentimentBreakdown;
}

export function SentimentBars({ sentiment }: SentimentBarsProps) {
  const theme = useTheme();

  const bars = [
    { key: "positive" as const, label: "Positive", color: theme.palette.success.main },
    { key: "neutral" as const, label: "Neutral", color: theme.palette.info.main },
    { key: "negative" as const, label: "Negative", color: theme.palette.error.main },
  ];

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      {bars.map(({ key, label, color }) => (
        <Box key={key}>
          <Box sx={{ display: "flex", justifyContent: "space-between", mb: 0.5 }}>
            <Typography variant="body2" color="textSecondary" sx={{ fontWeight: 500 }}>
              {label}
            </Typography>
            <Typography variant="body2" sx={{ fontWeight: 600, color }}>
              {sentiment[key]}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={sentiment[key]}
            sx={{
              height: 8,
              borderRadius: "4px",
              backgroundColor: theme.palette.divider,
              "& .MuiLinearProgress-bar": {
                backgroundColor: color,
              },
            }}
          />
        </Box>
      ))}
    </Box>
  );
}

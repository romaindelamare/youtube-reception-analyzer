import { Box, Paper, Typography, useTheme } from "@mui/material";

interface HighlightsListProps {
  highlights: string[];
}

export function HighlightsList({ highlights }: HighlightsListProps) {
  const theme = useTheme();

  if (highlights.length === 0) return null;

  const displayedHighlights = highlights.slice(0, 5);

  return (
    <Paper elevation={0} sx={{ p: 2, backgroundColor: theme.palette.background.paper, width: "100%" }}>
      <Typography
        variant="subtitle2"
        sx={{
          fontWeight: 700,
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          color: theme.palette.success.main,
          mb: 1.5,
        }}
      >
        Top Highlights
      </Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.75 }}>
        {displayedHighlights.map((h, i) => (
          <Box key={i} sx={{ display: "flex", gap: 1 }}>
            <Typography sx={{ fontSize: "0.875rem", color: "textSecondary", flexShrink: 0, pt: 0.25 }}>•</Typography>
            <Typography variant="body2" sx={{ lineHeight: 1.4 }}>
              {h}
            </Typography>
          </Box>
        ))}
      </Box>
    </Paper>
  );
}

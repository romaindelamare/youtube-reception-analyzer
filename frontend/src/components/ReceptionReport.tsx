import { Card, Box, Typography, Divider } from "@mui/material";
import type { AnalyzeResponse } from "../types/report";
import { ReceptionBadge } from "./ReceptionBadge";
import { SentimentChart } from "./SentimentChart";
import { ComplaintsList } from "./ComplaintsList";
import { HighlightsList } from "./HighlightsList";

interface ReceptionReportProps {
  report: AnalyzeResponse;
}

export function ReceptionReport({ report }: ReceptionReportProps) {
  return (
    <Card sx={{ mt: 3 }}>
      <Box sx={{ p: 3 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            mb: 2.5,
          }}
        >
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 0.5 }}>
              Overall Reception
            </Typography>
            <Typography variant="caption" color="textSecondary">
              Top {report.comments_analyzed} comments analyzed
            </Typography>
          </Box>
          <ReceptionBadge label={report.reception_label} />
        </Box>

        <Divider sx={{ my: 2.5 }} />

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
            gap: 3,
            mb: 2.5,
          }}
        >
          <Box>
            <SentimentChart sentiment={report.sentiment} />
          </Box>
          <Box
            sx={{
              p: 2,
              backgroundColor: (theme) =>
                theme.palette.mode === "dark"
                  ? "rgba(242, 132, 130, 0.08)"
                  : "rgba(211, 47, 47, 0.05)",
              borderLeft: "4px solid",
              borderColor: "primary.main",
              borderRadius: "0 8px 8px 0",
            }}
          >
            <Typography variant="body1" sx={{ lineHeight: 1.7 }}>
              {report.summary}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 2.5 }} />

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
            gap: 2,
          }}
        >
          <Box sx={{ display: "flex" }}>
            <ComplaintsList complaints={report.complaints} />
          </Box>
          <Box sx={{ display: "flex" }}>
            <HighlightsList highlights={report.highlights} />
          </Box>
        </Box>
      </Box>
    </Card>
  );
}

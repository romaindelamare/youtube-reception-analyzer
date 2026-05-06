import { Card, Box, Typography, Divider } from "@mui/material";
import type { AnalyzeResponse, AnalysisBlock } from "../types/report";
import { ReceptionBadge } from "./ReceptionBadge";
import { SentimentChart } from "./SentimentChart";
import { ComplaintsList } from "./ComplaintsList";
import { HighlightsList } from "./HighlightsList";

interface ReceptionReportProps {
  report: AnalyzeResponse;
}

function AnalysisBlockSection({
  title,
  block,
  comments_analyzed,
}: {
  title: string;
  block: AnalysisBlock;
  comments_analyzed: number;
}) {
  return (
    <Card sx={{ p: 3 }}>
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
            {title}
          </Typography>
          <Typography variant="caption" color="textSecondary">
            Based on top {comments_analyzed} comments
          </Typography>
        </Box>
        <ReceptionBadge label={block.reception_label} />
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
          <SentimentChart sentiment={block.sentiment} />
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
            {block.summary}
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
          <ComplaintsList complaints={block.complaints} />
        </Box>
        <Box sx={{ display: "flex" }}>
          <HighlightsList highlights={block.highlights} />
        </Box>
      </Box>
    </Card>
  );
}

export function ReceptionReport({ report }: ReceptionReportProps) {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3, mt: 3 }}>
      <AnalysisBlockSection
        title="Video Reception"
        block={report.video}
        comments_analyzed={report.comments_analyzed}
      />
      <AnalysisBlockSection
        title="Topic Reception"
        block={report.topic}
        comments_analyzed={report.comments_analyzed}
      />
    </Box>
  );
}

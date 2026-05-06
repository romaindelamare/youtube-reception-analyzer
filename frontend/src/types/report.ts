export interface SentimentBreakdown {
  positive: number;
  neutral: number;
  negative: number;
}

export interface AnalyzeResponse {
  reception_label: "Positive" | "Mixed" | "Negative";
  sentiment: SentimentBreakdown;
  complaints: string[];
  highlights: string[];
  summary: string;
  comments_analyzed: number;
}

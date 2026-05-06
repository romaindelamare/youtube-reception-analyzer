export interface SentimentBreakdown {
  positive: number;
  neutral: number;
  negative: number;
}

export interface AnalysisBlock {
  reception_label: "Positive" | "Mixed" | "Negative";
  sentiment: SentimentBreakdown;
  complaints: string[];
  highlights: string[];
  summary: string;
}

export interface AnalyzeResponse {
  video: AnalysisBlock;
  topic: AnalysisBlock;
  comments_analyzed: number;
}

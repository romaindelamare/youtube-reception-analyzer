import { useState, useMemo } from "react";
import {
  ThemeProvider,
  CssBaseline,
  Box,
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import { Brightness4, Brightness7 } from "@mui/icons-material";
import { lightTheme, darkTheme } from "./theme";
import { analyzeVideo } from "./api/analyzeVideo";
import { UrlInput } from "./components/UrlInput";
import { ReceptionReport } from "./components/ReceptionReport";
import type { AnalyzeResponse } from "./types/report";

type AppState = "idle" | "loading" | "result" | "error";

export default function App() {
  const [url, setUrl] = useState("");
  const [state, setState] = useState<AppState>("idle");
  const [report, setReport] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [darkMode, setDarkMode] = useState(() => {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  const theme = useMemo(() => (darkMode ? darkTheme : lightTheme), [darkMode]);

  const handleAnalyze = async () => {
    if (!url.trim()) return;
    setState("loading");
    setError(null);
    setReport(null);
    try {
      const data = await analyzeVideo(url.trim());
      setReport(data);
      setState("result");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setState("error");
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
        <AppBar position="fixed" elevation={1}>
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
              YouTube Reception Analyzer
            </Typography>
            <IconButton
              onClick={() => setDarkMode(!darkMode)}
              color="inherit"
              sx={{ ml: 2 }}
            >
              {darkMode ? <Brightness7 /> : <Brightness4 />}
            </IconButton>
          </Toolbar>
        </AppBar>

        <Toolbar />

        <Box
          sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            py: 4,
            px: 2,
          }}
        >
          <Container maxWidth="sm">
            {state !== "result" && (
              <Box sx={{ mb: 4, textAlign: "center" }}>
                <Typography variant="h4" component="h1" sx={{ mb: 1, fontWeight: 600 }}>
                  Analyze Video Reception
                </Typography>
                <Typography variant="body1" color="textSecondary">
                  Paste a YouTube URL to analyze how viewers received the video
                </Typography>
              </Box>
            )}

            <UrlInput
              value={url}
              onChange={setUrl}
              onSubmit={handleAnalyze}
              loading={state === "loading"}
            />

            {state === "loading" && (
              <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2, mt: 4 }}>
                <CircularProgress />
                <Typography color="textSecondary">
                  Scraping comments and analyzing with AI…
                </Typography>
              </Box>
            )}

            {state === "error" && (
              <Alert severity="error" sx={{ mt: 3 }}>
                {error}
              </Alert>
            )}
          </Container>

          {state === "result" && report && (
            <Container maxWidth="lg" sx={{ mx: "auto" }}>
              <ReceptionReport report={report} />
            </Container>
          )}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

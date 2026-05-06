import { Box, TextField, Button } from "@mui/material";

interface UrlInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}

export function UrlInput({ value, onChange, onSubmit, loading }: UrlInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !loading) onSubmit();
  };

  return (
    <Box sx={{ display: "flex", gap: 1.5, mb: 3 }}>
      <TextField
        type="text"
        placeholder="Paste a YouTube video URL..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        fullWidth
        variant="outlined"
        size="small"
      />
      <Button
        variant="contained"
        color="primary"
        onClick={onSubmit}
        disabled={loading || !value.trim()}
        sx={{ minWidth: "120px" }}
      >
        {loading ? "Analyzing…" : "Analyze"}
      </Button>
    </Box>
  );
}

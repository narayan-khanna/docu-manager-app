import { Box, Button, CircularProgress, Paper, TextField, Typography } from "@mui/material";
import { useState } from "react";
import api from "../services/api";

export default function QAPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await api.post("/qa", { question });
      setAnswer(res.data.answer);
      setSources(res.data.sources || []);
    } catch (err: any) {
      setAnswer(" Failed to get answer: " + (err?.response?.data?.detail || "Unknown error"));
      setSources([]);
    } finally {
      setLoading(false);
    }
  };

  // const askQuestion = async () => {
  //   try {
  //     const res = await api.post("/qa", {
  //       question,
  //       user_id: "narayan",  // optional if backend uses JWT info directly
  //     });
  //     setAnswer(res.data.answer);
  //   } catch (err: any) {
  //     setAnswer("Error: " + (err?.response?.data?.detail || "Something went wrong"));
  //   }
  // };

  return (
    <Box sx={{ maxWidth: 800, mx: "auto", mt: 6 }}>
      <Typography variant="h5" gutterBottom>🧠 Ask a Question</Typography>

      <TextField
        label="Your question"
        fullWidth
        multiline
        rows={3}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        sx={{ mb: 2 }}
      />

      <Button
        variant="contained"
        onClick={handleSubmit}
        disabled={!question || loading}
      >
        {loading ? <CircularProgress size={20} /> : "Ask"}
      </Button>

      {answer && (
        <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            💬 Answer:
          </Typography>
          <Typography>{answer}</Typography>

          {sources.length > 0 && (
            <>
              <Typography sx={{ mt: 3 }} variant="subtitle2">📚 Sources:</Typography>
              <ul>
                {sources.map((src, idx) => (
                  <li key={idx}>{src}</li>
                ))}
              </ul>
            </>
          )}
        </Paper>
      )}
    </Box>
  );
}

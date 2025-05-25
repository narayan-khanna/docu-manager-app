import {
  Box,
  Button,
  Checkbox,
  CircularProgress,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: "", error: false });
  const [docs, setDocs] = useState<any[]>([]); // Ideally you'd use a typed model
  const [selected, setSelected] = useState<string[]>([]);

  const handleUpload = async () => {

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await api.post("/ingest", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSnackbar({ open: true, message: `Ingested: ${res.data.doc_id}`, error: false });
      setFile(null);
      fetchDocs(); // Refresh list after upload
    } catch (err: any) {
      setSnackbar({
        open: true,
        message: err?.response?.data?.detail || "Upload failed",
        error: true
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchDocs = async () => {
    try {
      const res = await api.get("/documents");
      console.log("Document loaded ", res)
      setDocs(res.data);
    } catch {
      setDocs([]);
    }
  };

  const handleSelect = (docId: string) => {
    const newSelection = selected.includes(docId)
      ? selected.filter(id => id !== docId)
      : [...selected, docId];
    setSelected(newSelection);
  };

  const submitSelectedDocs = async () => {
    try {
      const res = await api.post("/select-docs", {
        user_id: "narayan", // Eventually this should be removed; server will use JWT
        doc_ids: selected
      });
      setSnackbar({ open: true, message: `Selected ${res.data.accepted_doc_ids.length} docs for QA`, error: false });
    } catch (e) {
      setSnackbar({ open: true, message: "Failed to submit document selection", error: true });
    }
  };

  useEffect(() => { fetchDocs(); }, []);


  return (
    <Box sx={{ maxWidth: 800, mx: "auto", mt: 5 }}>
      <Typography variant="h5" gutterBottom>📄 Upload Document File</Typography>
      <Typography variant="body2" sx={{ mb: 2 }}>
        Supported formats: PDF, DOCX, TXT, CSV, JSON
      </Typography>

      <input type="file" accept=".pdf,.docx,.txt,.csv,.json" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <Button variant="contained" sx={{ mt: 2, mb: 4 }} onClick={handleUpload} disabled={!file || loading}>
        {loading ? <CircularProgress size={20} color="inherit" /> : "Upload & Ingest"}
      </Button>

      <Typography variant="h6">📚 Uploaded Documents</Typography>

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Select</TableCell>
            <TableCell>Doc ID</TableCell>
            <TableCell>Timestamp</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {docs.map((doc, idx) => (
            <TableRow key={idx}>
              <TableCell>
                <Checkbox
                  checked={selected.includes(doc.doc_id)}
                  onChange={() => handleSelect(doc.doc_id)}
                />
              </TableCell>
              <TableCell>{doc.doc_id}</TableCell>
              <TableCell>{doc.timestamp}</TableCell>
              <TableCell>{doc.status}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Button
        variant="outlined"
        sx={{ mt: 2 }}
        onClick={submitSelectedDocs}
        disabled={selected.length === 0}
      >
        Use Selected Documents for Q&A
      </Button>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        message={snackbar.message}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        ContentProps={{ sx: { backgroundColor: snackbar.error ? "error.main" : "success.main" } }}
      />
    </Box>
  );
}

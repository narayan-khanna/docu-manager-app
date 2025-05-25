import {
  Box,
  CircularProgress,
  Paper,
  Typography,
  useTheme
} from "@mui/material";
import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis, YAxis
} from "recharts";
import api from "../services/api";

interface Metrics {
  documents_uploaded: { today: number; month: number; year: number };
  questions_asked: { today: number; month: number; year: number };
  documents_referred: { [doc_id: string]: number };
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const theme = useTheme();

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await api.get("/dashboard/metrics");
        setMetrics(res.data);
      } catch (e) {
        console.error("Failed to fetch dashboard metrics", e);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#f44336", "#2196f3", "#9c27b0"];

  const getBarData = (obj: { today: number; month: number; year: number }) => [
    { name: "Today", value: obj.today },
    { name: "Month", value: obj.month },
    { name: "Year", value: obj.year },
  ];

  const docRefData =
    metrics?.documents_referred
      ? Object.entries(metrics.documents_referred).map(([key, value]) => ({
          name: key,
          value,
        }))
      : [];

  if (loading) {
    return (
      <Box sx={{ mt: 8, display: "flex", justifyContent: "center" }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4, px: 4 }}>
      <Typography variant="h4" gutterBottom>
        📊 Usage Dashboard
      </Typography>

      {/* Flex container for charts */}
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 4 }}>

        {/* Documents Uploaded */}
        <Paper sx={{ flex: 1, minWidth: 300, p: 2 }}>
          <Typography variant="h6" gutterBottom>Documents Uploaded</Typography>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={getBarData(metrics!.documents_uploaded)}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill={theme.palette.primary.main} />
            </BarChart>
          </ResponsiveContainer>
        </Paper>

        {/* Questions Asked */}
        <Paper sx={{ flex: 1, minWidth: 300, p: 2 }}>
          <Typography variant="h6" gutterBottom>Questions Asked</Typography>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={getBarData(metrics!.questions_asked)}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill={theme.palette.success.main} />
            </BarChart>
          </ResponsiveContainer>
        </Paper>

        {/* Documents Referred */}
        {docRefData.length > 0 && (
          <Paper sx={{ flex: 1, minWidth: 300, p: 2 }}>
            <Typography variant="h6" gutterBottom>Documents Referred in Answers</Typography>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={docRefData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {docRefData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        )}
      </Box>
    </Box>
  );
}

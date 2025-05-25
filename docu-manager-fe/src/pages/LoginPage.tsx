import { Box, Button, TextField, Typography } from "@mui/material";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../auth/useAuth";

export default function LoginPage() {
  const { setToken } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://docu-manager-auth:8001/auth/login", {
        email, password
      });
      setToken(res.data.token);
      navigate("/");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <Box sx={{ maxWidth: 400, m: "auto", mt: 8 }}>
      <Typography variant="h5">Login</Typography>
      <TextField fullWidth label="Email" value={email} onChange={e => setEmail(e.target.value)} margin="normal" />
      <TextField fullWidth type="password" label="Password" value={password} onChange={e => setPassword(e.target.value)} margin="normal" />
      <Button fullWidth variant="contained" onClick={handleLogin} sx={{ mt: 2 }}>
        Login
      </Button>
    </Box>
  );
}

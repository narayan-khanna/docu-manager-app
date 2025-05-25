import { Box, List, ListItem, ListItemButton, ListItemText } from "@mui/material";
import { useNavigate } from "react-router-dom";

const menuItems = [
  { text: "Dashboard", path: "/" },
  { text: "Upload", path: "/upload" },
  { text: "Q&A", path: "/qa" },
  { text: "Users", path: "/users" },
];

export default function Sidebar() {
  const navigate = useNavigate();

  return (
    <Box sx={{ width: 200, background: "#f4f4f4", height: "100vh" }}>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => navigate(item.path)}>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}


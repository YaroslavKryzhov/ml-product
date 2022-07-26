import { Paper, Typography } from "@mui/material";
import { theme } from "globalStyle/theme";

export const UnavailableBlock: React.FC<{ label: string }> = ({ label }) => (
  <Paper
    elevation={3}
    sx={{
      color: theme.palette.primary.light,
      padding: theme.spacing(2),
      backgroundColor: theme.palette.secondary.light,
      borderRadius: theme.shape.borderRadius,
    }}
  >
    <Typography
      sx={{
        color: theme.palette.primary.light,
      }}
      variant="body1"
    >
      {label}
    </Typography>
  </Paper>
);

import {
  AppBar,
  Button,
  Checkbox,
  Chip,
  FormControlLabel,
  IconButton,
  Paper,
  Stack,
  TextField,
  Toolbar,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import React from "react";
import { CenteredContainer } from "components/muiOverride";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { changeEmail, changePasswordInput } from "ducks/reducers/auth";

export const Auth: React.FC = () => {
  const { passwordInput, emailInput } = useSESelector((state) => state.auth);
  const dispatch = useAppDispatch();

  return (
    <Stack direction="column" sx={{ height: "100vh" }}>
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Chip
            sx={{
              backgroundColor: "primary.light",
              color: "primary.contrastText",
              "&:hover": {
                backgroundColor: "secondary.dark",
              },
            }}
            clickable
            label="Регистрация"
          />
          <IconButton color="secondary" size="large">
            <MenuIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <CenteredContainer sx={{ flexGrow: 1 }}>
        <Paper sx={{ width: 657, p: "30px" }} elevation={3}>
          <Stack direction="column">
            <TextField
              size="small"
              type="email"
              label="Почта"
              value={emailInput}
              onChange={(e) => dispatch(changeEmail(e.target.value))}
              sx={{
                mb: "20px",
              }}
            />
            <TextField
              size="small"
              type="password"
              label="Пароль"
              value={passwordInput}
              onChange={(e) => dispatch(changePasswordInput(e.target.value))}
              sx={{
                mb: "20px",
              }}
            />
            <FormControlLabel
              control={<Checkbox size="small" />}
              label="Запомнить меня"
              sx={{
                mb: "10px",
              }}
            />
            <Button size="small" variant="contained">
              Войти
            </Button>
          </Stack>
        </Paper>
      </CenteredContainer>
    </Stack>
  );
};

import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import { Authentication } from "./app/Authentication";
import { useSESelector } from "ducks/hooks";
import { AppPage } from "ducks/reducers/types";
import { always, cond, equals, T } from "ramda";
import React from "react";
import "./globalStyle/app.scss";
import { theme } from "./globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";
import { Circles } from "react-loader-spinner";
import { withOpacity } from "./globalStyle/theme";
import { Workplace } from "./app/Workplace";
import { DialogCustom } from "components/Dialog";

const App: React.FC = () => {
  const { page, isBlockingLoader } = useSESelector((state) => state.main);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <DialogCustom />
      <Box sx={{ backgroundColor: "secondary.main" }}>
        {isBlockingLoader && (
          <CenteredContainer
            sx={{
              position: "fixed",
              height: "100vh",
              maxWidth: "100vw !important",
              zIndex: 100,
              bgcolor: (theme) => withOpacity(theme.palette.primary.main, 0.98),
            }}
          >
            <Circles width={100} color={theme.palette.secondary.dark} />
          </CenteredContainer>
        )}
        {cond<AppPage[], JSX.Element>([
          [equals<AppPage>(AppPage.Authentication), always(<Authentication />)],
          [equals<AppPage>(AppPage.Workplace), always(<Workplace />)],
          [T, always(<Authentication />)],
        ])(page)}
      </Box>
    </ThemeProvider>
  );
};

export default App;

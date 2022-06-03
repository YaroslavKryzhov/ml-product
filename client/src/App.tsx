import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import { Authentication } from "./app/Authentication";
import { Matcher, pathify, useSESelector } from "ducks/hooks";
import { AppPage } from "ducks/reducers/types";
import React from "react";
import "./globalStyle/app.scss";
import { theme } from "./globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";
import { Circles } from "react-loader-spinner";
import { withOpacity } from "./globalStyle/theme";
import { Workplace } from "./app/Workplace";
import { DialogCustom } from "components/Dialog";
import { Route, Routes } from "react-router";
import { BrowserRouter } from "react-router-dom";
import { Notices } from "app/Workplace/common/Notice";

const App: React.FC = () => {
  const { isBlockingLoader } = useSESelector((state) => state.main);

  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <DialogCustom />
        <Notices />
        <Box sx={{ backgroundColor: "secondary.main" }}>
          {isBlockingLoader && (
            <CenteredContainer
              sx={{
                position: "fixed",
                height: "100vh",
                maxWidth: "100vw !important",
                zIndex: 100,
                bgcolor: (theme) =>
                  withOpacity(theme.palette.primary.main, 0.98),
              }}
            >
              <Circles width={100} color={theme.palette.secondary.dark} />
            </CenteredContainer>
          )}

          <Routes>
            <Route
              path={pathify([AppPage.Authentication], {
                matcher: Matcher.start,
              })}
              element={<Authentication />}
            />
            <Route
              path={pathify([AppPage.Workplace], {
                matcher: Matcher.start,
              })}
              element={<Workplace />}
            />
            <Route path="/" element={<Authentication />} />
          </Routes>
        </Box>
      </ThemeProvider>
    </BrowserRouter>
  );
};

export default App;

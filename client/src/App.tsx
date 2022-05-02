import { Box, Stack, ThemeProvider } from "@mui/material";
import { Authentication } from "./app/Authentication";
import { useSESelector } from "ducks/hooks";
import { AppPage } from "ducks/reducers/types";
import { always, cond, equals, T } from "ramda";
import React from "react";
import "./globalStyle/app.scss";
import { theme } from "./globalStyle/theme";

const App: React.FC = () => {
  const { page } = useSESelector((state) => state.main);

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ backgroundColor: "secondary.main" }}>
        {cond<AppPage[], JSX.Element>([
          [equals<AppPage>(AppPage.Authentication), always(<Authentication />)],
          [T, always(<Authentication />)],
        ])(page)}
      </Box>
    </ThemeProvider>
  );
};

export default App;

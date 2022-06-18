import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "./redux/store";
import App from "./App";
import { css, Global } from "@emotion/react";
import JostFont from "./assets/fonts/Jost.ttf";

const container = document.getElementById("root")!;
const root = createRoot(container);

root.render(
  <Provider store={store}>
    <Global
      styles={css`
        body,
        html {
          margin: 0;
          padding: 0;
        }

        @font-face {
          font-family: Jost;
          src: url(${JostFont}) format("truetype");
        }
      `}
    />
    <App />
  </Provider>
);

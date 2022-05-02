import * as React from "react";
import { styled } from "@mui/material/styles";
import Container, { ContainerProps } from "@mui/material/Container";

export const CenteredContainer = styled(Container)<ContainerProps>(() => ({
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
}));

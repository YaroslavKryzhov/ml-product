import * as React from "react";
import { styled } from "@mui/material/styles";
import Container, { ContainerProps } from "@mui/material/Container";
import { theme } from "globalStyle/theme";

export const CenteredContainer = styled(Container)<ContainerProps>(() => ({
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
}));

export const helperTextProps = {
  sx: {
    position: "absolute",
    top: "44px",
    mt: 0,
    fontSize: theme.typography.caption.fontSize!,
    lineHeight: theme.typography.caption.fontSize!,
  },
};

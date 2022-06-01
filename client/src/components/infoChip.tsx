import styled from "@emotion/styled";
import { Box } from "@mui/material";
import { theme } from "globalStyle/theme";
import React from "react";
import { Size } from "app/types";

export const StyledBox = styled.div<{ size?: Size }>`
  width: min-content;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${({ size }) =>
    size === Size.small
      ? `${theme.spacing(0.1)} ${theme.spacing(1)}`
      : theme.spacing(2)};
  white-space: nowrap;
  font-size: ${({ size }) =>
    size === Size.small ? theme.typography.caption.fontSize : "inherit"};

  &:first-of-type {
    background-color: ${theme.palette.primary.dark};
    color: ${theme.palette.primary.contrastText};
    border-radius: ${theme.shape.borderRadiusRound}px 0 0
      ${theme.shape.borderRadiusRound}px;
  }
  &:last-of-type {
    border: ${theme.additional.borderWidth}px solid
      ${theme.palette.primary.dark};
    border-radius: 0 ${theme.shape.borderRadiusRound}px
      ${theme.shape.borderRadiusRound}px 0;
  }
`;

export const InfoChip: React.FC<{
  label: string;
  info: React.ReactNode;
  size?: Size;
}> = ({ label, info, size }) => {
  return (
    <Box
      sx={{
        display: "flex",
      }}
    >
      <StyledBox size={size}>{label}</StyledBox>
      <StyledBox size={size}>{info}</StyledBox>
    </Box>
  );
};

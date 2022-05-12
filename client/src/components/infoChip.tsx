import styled from "@emotion/styled";
import { Box } from "@mui/material";
import { theme } from "globalStyle/theme";
import React from "react";

export const StyledBox = styled.div`
  width: min-content;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${theme.spacing(2)};
  white-space: nowrap;

  &:first-child {
    background-color: ${theme.palette.primary.dark};
    color: ${theme.palette.primary.contrastText};
    border-radius: ${theme.shape.borderRadiusRound}px 0 0
      ${theme.shape.borderRadiusRound}px;
  }
  &:last-child {
    border: ${theme.additional.borderWidth}px solid
      ${theme.palette.primary.dark};
    border-radius: 0 ${theme.shape.borderRadiusRound}px
      ${theme.shape.borderRadiusRound}px 0;
  }
`;

export const InfoChip: React.FC<{
  label: string;
  info: React.ReactNode;
}> = ({ label, info }) => {
  return (
    <Box
      sx={{
        display: "flex",
      }}
    >
      <StyledBox>{label}</StyledBox>
      <StyledBox>{info}</StyledBox>
    </Box>
  );
};

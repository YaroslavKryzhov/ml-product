import styled from "@emotion/styled";
import { theme } from "globalStyle/theme";

const fixedTableCellStyles = `
  position: sticky!important;
  left: 0;
  text-align: left;
  border-right: ${theme.additional.borderWidth} solid ${theme.palette.secondary.dark};
  z-index: 1;
  background-color: ${theme.palette.secondary.light};
`;

export const StyledTable = styled.table<{
  maxHeight?: string;
  isFirstColumnFixed?: boolean;
  width?: number;
}>`
  min-width: unset !important;
  display: block;
  position: relative;
  border-collapse: collapse;
  max-height: ${({ maxHeight }) => maxHeight || "none"};
  overflow-y: ${({ maxHeight }) => (maxHeight ? "auto" : "hidden")};
  overflow-x: scroll;
  max-width: 100%;

  tbody tr td:first-of-type {
    ${({ isFirstColumnFixed }) => isFirstColumnFixed && fixedTableCellStyles}
    justify-content: flex-start;
  }

  thead tr th:first-of-type {
    ${({ isFirstColumnFixed }) => isFirstColumnFixed && fixedTableCellStyles}
    justify-content: flex-start;

    div {
      ${({ isFirstColumnFixed }) => isFirstColumnFixed && `text-align: left;`}
    }
  }
`;

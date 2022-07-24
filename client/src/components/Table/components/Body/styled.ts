import styled from "@emotion/styled";
import { theme } from "globalStyle/theme";
import { Fixed } from "../../types";

export const StyledTableRow = styled.tr<{ rowHoverable?: boolean }>`
  .speedDial {
    display: none;
  }
  cursor: pointer;
  ${(rowHoverable) =>
    rowHoverable &&
    `&:hover{
    background-color: ${theme.palette.divider};
    .speedDial{
      display: flex;
    }
  }`}
`;

export const CellValueContainer = styled.div`
  overflow: hidden;
  text-overflow: ellipsis;
  position: relative;
  white-space: nowrap;
`;

export const StyledTableCell = styled.td<{
  fixed?: Fixed;
  compact?: boolean;
  offCellsPaddings?: boolean;
}>`
  padding: ${({ compact, offCellsPaddings }) =>
    offCellsPaddings
      ? "none"
      : compact
      ? `${theme.spacing(0.2)} ${theme.spacing(1)}`
      : `${theme.spacing(2)} ${theme.spacing(3)}`};
  display: flex;
  align-items: center;
  border-bottom: ${theme.additional.borderWidth} solid ${theme.palette.divider};
  font-size: ${theme.typography.body2.fontSize};

  justify-content: ${({ fixed }) => {
    if (fixed) {
      return fixed === Fixed.right
        ? "flex-end"
        : fixed === Fixed.left
        ? "flex-start"
        : "center";
    }

    return "center";
  }};

  &:last-of-type {
    justify-content: flex-end;
  }

  &:first-of-type {
    justify-content: flex-start;
  }
`;

export const EmptyData = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center !important;
  padding: ${theme.spacing(3)} 0;
  flex-grow: 1;
`;

export const TableFixContainer = styled.tbody`
  border: ${theme.additional.borderWidth} solid ${theme.shadows[11]};
`;

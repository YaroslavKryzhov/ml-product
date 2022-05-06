import styled from "@emotion/styled";
import { theme } from "globalStyle/theme";
import { Fixed } from "../../types";

export const StyledTableRow = styled.tr``;

export const StyledTableCell = styled.td<{
  fixed?: Fixed;
}>`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: ${theme.spacing(2)} ${theme.spacing(3)};
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

  &:last-child {
    justify-content: flex-end;
  }

  &:first-child {
    justify-content: flex-start;
  }
`;

export const EmptyData = styled.td`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center !important;
  padding: ${theme.spacing(3)} 0;
`;

export const TableFixContainer = styled.tbody`
  border: ${theme.additional.borderWidth} solid ${theme.shadows[11]};
`;

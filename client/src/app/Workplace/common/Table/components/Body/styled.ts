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
  padding: 10px 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid ${theme.palette.divider};
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

export const EmptyData = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px 0;
`;

export const TableFixContainer = styled.tbody`
  border: 1px solid ${theme.shadows[11]};
`;

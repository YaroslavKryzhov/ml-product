import styled from "@emotion/styled";
import { theme } from "globalStyle/theme";
import { Fixed } from "../../types";
import arrowUpIcon from "../../icons/arrow-up.svg";

export const StyledTableHead = styled.thead`
  z-index: 10;
  position: sticky !important;
  left: 0;
  top: 0;
  background-color: ${theme.palette.secondary.light};
`;

export const StyledHeadCell = styled.th<{
  resizable?: boolean;
  fixed?: Fixed;
  borderRight?: boolean;
  borderLeft?: boolean;
}>`
  user-select: none;
  position: relative;
  font-weight: ${theme.typography.fontWeightBold};
  display: flex;
  padding: 4px 20px;
  font-size: ${theme.typography.body1.fontSize};
  border-bottom: 1px solid ${theme.palette.divider};
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

export const HeadCellContent = styled.div`
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
  width: min-content;
`;

export const SortedArrowUp = styled.span<{ isFlipped?: boolean }>`
  position: relative;
  margin-left: 10px;
  top: 50%;
  background: url(${arrowUpIcon}) no-repeat center;
  transform: translateY(-50%)
    ${({ isFlipped }) => (isFlipped ? "rotate(180deg)" : "")};
  width: 9px;
  height: 5px;
`;

export const StyledResizer = styled.span<{ resizable?: boolean }>`
  bottom: 0;
  cursor: ${({ resizable }) => (resizable ? "col-resize" : "pointer")};
  position: absolute;
  right: 0;
  top: 0;
  transform: translateX(50%);
  width: 36px;
  z-index: 2;

  &:after {
    content: "";
    border-right: 1px solid ${theme.palette.secondary.dark};
    position: absolute;
    left: 18px;
    top: 0;
    height: 100%;
  }
`;

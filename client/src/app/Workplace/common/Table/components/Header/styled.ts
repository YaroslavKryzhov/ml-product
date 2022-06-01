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
  offHeaderPaddings?: boolean;
  compact?: boolean;
}>`
  text-overflow: ellipsis;
  white-space: nowrap;
  user-select: none;
  position: relative;
  font-weight: ${theme.typography.fontWeightBold};
  display: flex;
  padding: ${({ offHeaderPaddings, compact }) =>
    offHeaderPaddings
      ? "none"
      : compact
      ? `${theme.spacing(1)} ${theme.spacing(1)}`
      : `${theme.spacing(1)} ${theme.spacing(3)}`};
  font-size: ${theme.typography.body1.fontSize};
  border-bottom: ${theme.additional.borderWidth} solid ${theme.palette.divider};
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

export const HeadCellContent = styled.div`
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
  width: min-content;
  display: block;
`;

export const SortedArrowUp = styled.span<{ isFlipped?: boolean }>`
  position: relative;
  margin-left: ${theme.spacing(2)};
  top: 52%;
  background-color: ${theme.palette.primary.main};
  transform: translateY(-50%)
    ${({ isFlipped }) => (isFlipped ? "rotate(180deg)" : "")};
  mask-image: url(${arrowUpIcon});
  -webkit-mask-image: url(${arrowUpIcon});
  mask-repeat: no-repeat;
  mask-position: center;
  mask-size: contain;
  width: 12px;
  height: 9px;
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
    border-right: ${theme.additional.borderWidth} solid
      ${theme.palette.secondary.dark};
    position: absolute;
    left: 18px;
    top: 0;
    height: 100%;
  }
`;

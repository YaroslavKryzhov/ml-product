import { emphasize, styled } from "@mui/material/styles";
import Chip from "@mui/material/Chip";
import { Slide, SlideProps } from "@mui/material";
import styledEmption from "@emotion/styled";
import { theme } from "globalStyle/theme";

export const StyledBreadcrumb = styled(Chip)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.dark,
  height: theme.spacing(3),
  fontWeight: theme.typography.fontWeightRegular,
  cursor: "pointer",
  "&:hover, &:focus": {
    backgroundColor: emphasize(theme.palette.secondary.dark, 0.2),
  },
  "&:active": {
    boxShadow: theme.shadows[1],
    backgroundColor: emphasize(theme.palette.secondary.dark, 0.3),
  },
})) as typeof Chip;

export const SlideTr = (props: SlideProps) => (
  <Slide {...props} direction={"left"} />
);

export const EditableLabel = styledEmption.label<{ editMode?: boolean }>`
  &:focus-visible {
    outline: none;
  }
  ${({ editMode }) =>
    editMode &&
    `border-bottom: ${theme.additional.borderWidth}px solid ${theme.palette.primary.main};`}
`;

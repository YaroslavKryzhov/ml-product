import { Snackbar, Typography } from "@mui/material";
import { theme } from "globalStyle/theme";
import { useEffect, useState } from "react";
import ErrorIcon from "@mui/icons-material/Error";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { SlideTr } from "./styled";
import { removeNotice, SnackBarType } from "ducks/reducers/notices";
import { useAppDispatch, useSESelector } from "ducks/hooks";

const TypeToColor = {
  [SnackBarType.error]: theme.palette.error.main,
  [SnackBarType.success]: theme.palette.success.main,
};

const Notice: React.FC<{
  id: number | string;
  type: SnackBarType;
  label: string;
}> = ({ type, label, id }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dispatch = useAppDispatch();

  useEffect(() => setIsOpen(true), []);

  return (
    <Snackbar
      autoHideDuration={3000}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      open={isOpen}
      onClose={() => {
        setIsOpen(false);
        setTimeout(
          () => dispatch(removeNotice(id)),
          theme.transitions.duration.leavingScreen
        );
      }}
      message={
        <Typography
          variant="body2"
          sx={{
            color: TypeToColor[type],
            display: "flex",
            gap: theme.spacing(1),
            alignItems: "center",
          }}
        >
          {type === SnackBarType.error && <ErrorIcon />}
          {type === SnackBarType.success && <CheckCircleIcon />}
          {label}
        </Typography>
      }
      TransitionComponent={SlideTr}
    />
  );
};

export const Notices: React.FC = () => {
  const notices = useSESelector((state) => state.notices);

  return (
    <div>
      {notices.map((note) => (
        <Notice key={note.id} {...note} />
      ))}
    </div>
  );
};

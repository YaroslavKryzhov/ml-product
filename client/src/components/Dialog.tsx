import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { useEffect, useState } from "react";
import { setDialog } from "ducks/reducers/dialog";

const Transition = React.forwardRef(
  (
    props: TransitionProps & {
      children: React.ReactElement;
    },
    ref: React.Ref<unknown>
  ) => <Slide direction="up" ref={ref} {...props} />
);

export type DialogProps = {
  onAccept?: () => void;
  onDismiss?: () => void;
  close: () => void;
  title: string | null;
  text?: string;
  acceptText?: string;
  dismissText?: string;
};

export const DialogCustom: React.FC = () => {
  const { onAccept, onDismiss, title, text, acceptText, dismissText } =
    useSESelector((state) => state.dialog);
  const [open, setIsOpen] = useState(false);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (title) setIsOpen(true);
  }, [title]);

  const close = () => {
    setIsOpen(false);
    dispatch(setDialog({ title: null }));
  };

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      keepMounted
      onClose={close}
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{text}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => {
            onDismiss && onDismiss();
            close();
          }}
        >
          {dismissText || "Нет"}
        </Button>
        <Button
          onClick={() => {
            onAccept && onAccept();
            close();
          }}
        >
          {acceptText || "Да"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

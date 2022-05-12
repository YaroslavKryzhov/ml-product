import * as React from "react";
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
import { theme } from "globalStyle/theme";
import { LoadingButton } from "@mui/lab";

export const CustomTransition = React.forwardRef(
  (
    props: TransitionProps & {
      children: React.ReactElement;
    },
    ref: React.Ref<unknown>
  ) => <Slide direction="up" ref={ref} {...props} />
);

export type DialogProps = {
  onAccept?: () => Promise<void>;
  onDismiss?: () => void;
  onClose?: () => void;
  title: string | null;
  text?: string;
  acceptText?: string;
  dismissText?: string;
  Content?: React.ReactElement;
  acceptDisabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
};

export const DialogCustom: React.FC = () => {
  const {
    onAccept,
    onDismiss,
    onClose,
    title,
    text,
    acceptText,
    dismissText,
    Content,
    acceptDisabled,
    loading,
    fullWidth,
  } = useSESelector((state) => state.dialog);
  const [open, setIsOpen] = useState(false);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (title) setIsOpen(true);
  }, [title]);

  const close = () => {
    setIsOpen(false);
    dispatch(setDialog({ title: null }));
    onClose && onClose();
  };

  return (
    <Dialog
      open={open}
      TransitionComponent={CustomTransition}
      keepMounted
      onClose={close}
      sx={{
        "& .MuiDialog-paper": {
          p: theme.spacing(1),
          maxWidth: "100vw",
          width: fullWidth ? "100%" : "auto",
        },
      }}
    >
      <DialogTitle sx={{ textAlign: "center" }} variant="h5">
        {title}
      </DialogTitle>
      <DialogContent>
        {Content || (
          <DialogContentText sx={{ textAlign: "center" }}>
            {text}
          </DialogContentText>
        )}
      </DialogContent>
      {(onDismiss || onAccept) && (
        <DialogActions
          sx={{
            mr: theme.spacing(2),
            ml: theme.spacing(2),
            gap: theme.spacing(2),
            justifyContent: "center",
          }}
        >
          {onAccept && (
            <LoadingButton
              loading={loading}
              disabled={acceptDisabled}
              size="small"
              variant="contained"
              onClick={() => {
                onAccept ? onAccept().then(() => close()) : close();
              }}
            >
              {acceptText || "Да"}
            </LoadingButton>
          )}
          {onDismiss && (
            <LoadingButton
              loading={loading}
              size="small"
              variant="contained"
              onClick={() => {
                onDismiss && onDismiss();
                close();
              }}
            >
              {dismissText || "Нет"}
            </LoadingButton>
          )}
        </DialogActions>
      )}
    </Dialog>
  );
};

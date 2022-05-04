import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import { createRoot } from "react-dom/client";

export const DialogContainerClass = "custom-dialog-container";

const Transition = React.forwardRef(
  (
    props: TransitionProps & {
      children: React.ReactElement;
    },
    ref: React.Ref<unknown>
  ) => <Slide direction="up" ref={ref} {...props} />
);

type DialogProps = {
  onAccept?: () => void;
  onDismiss?: () => void;
  close: () => void;
  title: string;
  text?: string;
  acceptText?: string;
  dismissText?: string;
};

const DialogCustom: React.FC<DialogProps> = ({
  onAccept,
  onDismiss,
  title,
  text,
  acceptText,
  dismissText,
  close,
}) => (
  <Dialog open TransitionComponent={Transition} keepMounted onClose={close}>
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

export const ShowDialog = (props: Omit<DialogProps, "close">) => {
  const portal: HTMLDivElement | null = document.querySelector(
    `.${DialogContainerClass}`
  );

  if (!portal) return;

  const root = createRoot(portal);

  const closeModal = () => root.unmount();
  if (portal) root.render(<DialogCustom {...props} close={closeModal} />);

  return closeModal;
};

import { Snackbar, Typography } from "@mui/material";
import { theme } from "globalStyle/theme";
import { useState } from "react";
import { createRoot } from "react-dom/client";
import { SlideTr } from "./styled";

export enum SnackBarType {
  error = "error",
}

const TypeToColor = {
  [SnackBarType.error]: theme.palette.error.main,
};

export const NOTICE_CONTAINER_ID = "NOTICE_CONTAINER_ID";

export const useNotice = ({
  label,
  type,
}: {
  label: string;
  type: SnackBarType;
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const Notice = () => (
    <Snackbar
      autoHideDuration={3000}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      open={isOpen}
      onClose={() => setIsOpen(false)}
      message={
        <Typography variant="body2" sx={{ color: TypeToColor[type] }}>
          {label}
        </Typography>
      }
      TransitionComponent={SlideTr}
    />
  );

  const container = document.getElementById(NOTICE_CONTAINER_ID);

  if (container) {
    const root = createRoot(container);

    root.render(<Notice />);
  }

  return setIsOpen;
};

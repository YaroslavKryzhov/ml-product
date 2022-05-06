import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { DialogProps } from "components/Dialog";

const initialState: DialogProps = {
  title: null,
};

const dialogSlice = createSlice({
  name: "dialog",
  initialState,
  reducers: {
    setDialog: (_, action: PayloadAction<DialogProps>) => action.payload,
    setDialogAcceptDisabled: (state, action: PayloadAction<boolean>) =>
      void (state.acceptDisabled = action.payload),
    setDialogLoading: (state, action: PayloadAction<boolean>) =>
      void (state.loading = action.payload),
  },
});

export const { setDialog, setDialogAcceptDisabled, setDialogLoading } =
  dialogSlice.actions;

export default dialogSlice.reducer;

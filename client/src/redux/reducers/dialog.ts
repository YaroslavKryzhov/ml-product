import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { DialogProps } from "components/Dialog";

type DialogSliceProps = Omit<DialogProps, "close">;

const initialState: DialogSliceProps = {
  title: null,
};

const dialogSlice = createSlice({
  name: "dialog",
  initialState,
  reducers: {
    setDialog: (_, action: PayloadAction<DialogSliceProps>) => action.payload,
  },
});

export const { setDialog } = dialogSlice.actions;

export default dialogSlice.reducer;

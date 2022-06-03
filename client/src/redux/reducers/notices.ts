import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export enum SnackBarType {
  error = "error",
  success = "success",
}

export type Notice = { label: string; type: SnackBarType; id: string | number };

const initialState: Notice[] = [];

const noticesSlice = createSlice({
  name: "notices",
  initialState,
  reducers: {
    addNotice: (state, action: PayloadAction<Notice>) =>
      void state.push(action.payload),
    removeNotice: (state, action: PayloadAction<number | string>) =>
      state.filter((x) => x.id !== action.payload),
  },
});

export const { addNotice, removeNotice } = noticesSlice.actions;

export default noticesSlice.reducer;

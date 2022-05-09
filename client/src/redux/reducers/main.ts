import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { MainSlice } from "./types";

const initialState: MainSlice = {
  isBlockingLoader: true,
};

const mainSlice = createSlice({
  name: "main",
  initialState,
  reducers: {
    changeIsBlockingLoader: (state, action: PayloadAction<boolean>) =>
      void (state.isBlockingLoader = action.payload),
  },
});

export const { changeIsBlockingLoader } = mainSlice.actions;

export default mainSlice.reducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { MainSlice, WorkPage } from "./types";

const initialState: MainSlice = {
  workPage: WorkPage.Documents,
  isBlockingLoader: true,
};

const mainSlice = createSlice({
  name: "main",
  initialState,
  reducers: {
    changeWorkPage: (state, action: PayloadAction<WorkPage>) =>
      void (state.workPage = action.payload),
    changeIsBlockingLoader: (state, action: PayloadAction<boolean>) =>
      void (state.isBlockingLoader = action.payload),
  },
});

export const { changeIsBlockingLoader, changeWorkPage } = mainSlice.actions;

export default mainSlice.reducer;

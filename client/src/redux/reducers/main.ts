import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AppPage, MainSlice, WorkPage } from "./types";

const initialState: MainSlice = {
  page: AppPage.Authentication,
  workPage: WorkPage.Documents,
  isBlockingLoader: true,
};

const mainSlice = createSlice({
  name: "main",
  initialState,
  reducers: {
    changeAppPage: (state, action: PayloadAction<AppPage>) =>
      void (state.page = action.payload),
    changeWorkPage: (state, action: PayloadAction<WorkPage>) =>
      void (state.workPage = action.payload),
    changeIsBlockingLoader: (state, action: PayloadAction<boolean>) =>
      void (state.isBlockingLoader = action.payload),
    logout: (state) => {
      localStorage.authToken = "";
      state.page = AppPage.Authentication;
    },
  },
});

export const { changeAppPage, logout, changeIsBlockingLoader, changeWorkPage } =
  mainSlice.actions;

export default mainSlice.reducer;

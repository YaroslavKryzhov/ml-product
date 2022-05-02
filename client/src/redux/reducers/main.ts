import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AppPage, MainSlice } from "./types";

const initialState: MainSlice = {
  page: AppPage.Authentication,
  isBlockingLoader: true,
};

const mainSlice = createSlice({
  name: "main",
  initialState,
  reducers: {
    changeAppPage: (state, action: PayloadAction<AppPage>) =>
      void (state.page = action.payload),
    changeIsBlockingLoader: (state, action: PayloadAction<boolean>) =>
      void (state.isBlockingLoader = action.payload),
    logout: (state) => {
      localStorage.authToken = "";
      state.page = AppPage.Authentication;
    },
  },
});

export const { changeAppPage, logout, changeIsBlockingLoader } =
  mainSlice.actions;

export default mainSlice.reducer;

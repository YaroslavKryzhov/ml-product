import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AppPage, MainSlice } from "./types";

const initialState: MainSlice = {
  page: AppPage.Authentication,
};

const mainSlice = createSlice({
  name: "main",
  initialState,
  reducers: {
    changeAppPage: (state, action: PayloadAction<AppPage>) =>
      void (state.page = action.payload),
    logout: (state) => {
      localStorage.authToken = "";
      state.page = AppPage.Authentication;
    },
  },
});

export const { changeAppPage, logout } = mainSlice.actions;

export default mainSlice.reducer;

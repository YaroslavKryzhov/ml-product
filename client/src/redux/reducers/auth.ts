import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AuthPage, AuthSlice } from "./types";

const initialState: AuthSlice = {
  page: AuthPage.auth,
  passwordInput: "",
  secondPasswordInput: "",
  emailInput: "",
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    changePasswordInput: (state, action: PayloadAction<string>) =>
      void (state.passwordInput = action.payload),
    changeSecondPasswordInput: (state, action: PayloadAction<string>) =>
      void (state.secondPasswordInput = action.payload),
    changeAuthPage: (_, action: PayloadAction<AuthPage>) => ({
      ...initialState,
      page: action.payload,
    }),
    changeEmail: (state, action: PayloadAction<string>) =>
      void (state.emailInput = action.payload),
  },
});

export const {
  changePasswordInput,
  changeAuthPage,
  changeSecondPasswordInput,
  changeEmail,
} = authSlice.actions;

export default authSlice.reducer;

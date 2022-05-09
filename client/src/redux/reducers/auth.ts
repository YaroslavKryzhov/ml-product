import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { authApi } from "./api/auth.api";
import { AuthSlice } from "./types";

const initialState: AuthSlice = {
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

    changeEmail: (state, action: PayloadAction<string>) =>
      void (state.emailInput = action.payload),
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(authApi.endpoints.auth.matchFulfilled, (state) => {
        state.emailInput = "";
        state.passwordInput = "";
      })
      .addMatcher(authApi.endpoints.register.matchFulfilled, (state) => {
        state.emailInput = "";
        state.passwordInput = "";
        state.secondPasswordInput = "";
      });
  },
});

export const { changePasswordInput, changeSecondPasswordInput, changeEmail } =
  authSlice.actions;

export default authSlice.reducer;

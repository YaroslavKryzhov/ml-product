import { createSlice, PayloadAction } from "@reduxjs/toolkit";
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
    authReset: (state) => {
      state.emailInput = "";
      state.passwordInput = "";
      state.secondPasswordInput = "";
    },
  },
});

export const {
  changePasswordInput,
  changeSecondPasswordInput,
  changeEmail,
  authReset,
} = authSlice.actions;

export default authSlice.reducer;

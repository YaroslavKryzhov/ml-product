import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type CompositionsSlice = {
  customCompositionName: string;
};

const initialState: CompositionsSlice = {
  customCompositionName: "",
};

const compositionsSlice = createSlice({
  name: "compositions",
  initialState,
  reducers: {
    changeCustomCompositionName: (state, action: PayloadAction<string>) =>
      void (state.customCompositionName = action.payload),
  },
});

export const { changeCustomCompositionName } = compositionsSlice.actions;

export default compositionsSlice.reducer;

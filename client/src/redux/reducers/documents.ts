import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { DocumentsSlice } from "./types";

const initialState: DocumentsSlice = {};

const documentsSlice = createSlice({
  name: "documents",
  initialState,
  reducers: {},
});

export const {} = documentsSlice.actions;

export default documentsSlice.reducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { DocumentPage, DocumentsSlice } from "./types";

const initialState: DocumentsSlice = {
  page: DocumentPage.List,
};

const documentsSlice = createSlice({
  name: "documents",
  initialState,
  reducers: {
    changeDocumentPage: (state, action: PayloadAction<DocumentPage>) =>
      void (state.page = action.payload),
  },
});

export const { changeDocumentPage } = documentsSlice.actions;

export default documentsSlice.reducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { DocumentPage } from "./types";

export type DocumentsSlice = {
  page: DocumentPage;
  customFileName: string;
  selectedFile: File | null;
};

const initialState: DocumentsSlice = {
  page: DocumentPage.List,
  customFileName: "",
  selectedFile: null,
};

const documentsSlice = createSlice({
  name: "documents",
  initialState,
  reducers: {
    changeDocumentPage: (state, action: PayloadAction<DocumentPage>) =>
      void (state.page = action.payload),
    changeCustomFileName: (state, action: PayloadAction<string>) =>
      void (state.customFileName = action.payload),
    changeSelectedFile: (state, action: PayloadAction<File | null>) =>
      void (state.selectedFile = action.payload),
  },
});

export const { changeDocumentPage, changeCustomFileName, changeSelectedFile } =
  documentsSlice.actions;

export default documentsSlice.reducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type DocumentsSlice = {
  customFileName: string;
  selectedFile: File | null;
};

const initialState: DocumentsSlice = {
  customFileName: "",
  selectedFile: null,
};

const documentsSlice = createSlice({
  name: "documents",
  initialState,
  reducers: {
    changeCustomFileName: (state, action: PayloadAction<string>) =>
      void (state.customFileName = action.payload),
    changeSelectedFile: (state, action: PayloadAction<File | null>) =>
      void (state.selectedFile = action.payload),
  },
});

export const { changeCustomFileName, changeSelectedFile } =
  documentsSlice.actions;

export default documentsSlice.reducer;

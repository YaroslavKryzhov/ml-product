import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { TaskType } from "./types";

export type DocumentsSlice = {
  customFileName: string;
  selectedFile: File | null;
  selectedTargetColumn: string | null;
  selectedTaskType: TaskType | null;
};

const initialState: DocumentsSlice = {
  customFileName: "",
  selectedFile: null,
  selectedTargetColumn: null,
  selectedTaskType: null,
};

const documentsSlice = createSlice({
  name: "documents",
  initialState,
  reducers: {
    changeCustomFileName: (state, action: PayloadAction<string>) =>
      void (state.customFileName = action.payload),
    changeSelectedFile: (state, action: PayloadAction<File | null>) =>
      void (state.selectedFile = action.payload),
    changeSelectedTarget: (state, action: PayloadAction<string | null>) =>
      void (state.selectedTargetColumn = action.payload),
    changeSelectedTaskType: (state, action: PayloadAction<TaskType | null>) =>
      void (state.selectedTaskType = action.payload),
  },
});

export const {
  changeCustomFileName,
  changeSelectedFile,
  changeSelectedTarget,
  changeSelectedTaskType,
} = documentsSlice.actions;

export default documentsSlice.reducer;

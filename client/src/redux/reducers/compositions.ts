import { createSlice, nanoid, PayloadAction } from "@reduxjs/toolkit";
import {
  CompositionType,
  Model,
  ParamsCompositionType,
  TaskType,
} from "./types";

export type CompositionsSlice = {
  customCompositionName: string;
  models: Record<string, Model>;
  taskType?: TaskType;
  compositionType?: CompositionType;
  paramsType?: ParamsCompositionType;
  dataframeId: string | null;
  predictDataframeId: string | null;
  testSize: number;
};

const initialState: CompositionsSlice = {
  customCompositionName: "",
  models: {},
  dataframeId: null,
  predictDataframeId: null,
  testSize: 0.2,
  taskType: TaskType.classification,
  compositionType: CompositionType.none,
  paramsType: ParamsCompositionType.default,
};

const compositionsSlice = createSlice({
  name: "compositions",
  initialState,
  reducers: {
    changeCustomCompositionName: (state, action: PayloadAction<string>) =>
      void (state.customCompositionName = action.payload),
    changeTaskType: (state, action: PayloadAction<TaskType>) =>
      void (state.taskType = action.payload),
    changeCompositionType: (state, action: PayloadAction<CompositionType>) =>
      void (state.compositionType = action.payload),
    changeParamsType: (state, action: PayloadAction<ParamsCompositionType>) =>
      void (state.paramsType = action.payload),
    changeDataframeId: (state, action: PayloadAction<string>) =>
      void (state.dataframeId = action.payload),
    changePredictDataframeId: (state, action: PayloadAction<string>) =>
      void (state.predictDataframeId = action.payload),
    changeTestSize: (state, action: PayloadAction<number>) =>
      void (state.testSize = action.payload),
    addModel: (state) =>
      void (state.models[nanoid()] = { type: null, params: null }),
    deleteModel: (state, { payload }: PayloadAction<string>) =>
      void (state.models = Object.fromEntries(
        Object.entries(state.models).filter(([id]) => id !== payload)
      )),
    setModels: (state, { payload }: PayloadAction<Model[]>) =>
      void (state.models = Object.fromEntries(
        payload.map((x) => [nanoid(), x])
      )),
    changeModel: (state, action: PayloadAction<{ id: string; model: Model }>) =>
      void (state.models[action.payload.id] = action.payload.model),
    resetComposition: () => initialState,
  },
});

export const {
  changeCustomCompositionName,
  changeTaskType,
  changeCompositionType,
  changeParamsType,
  changeDataframeId,
  changePredictDataframeId,
  changeTestSize,
  addModel,
  deleteModel,
  changeModel,
  resetComposition,
  setModels,
} = compositionsSlice.actions;

export default compositionsSlice.reducer;

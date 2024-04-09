import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { IDataframe, IJob, IModel, ISimpleDataframe } from "@/utils/types";

interface DataframeState {
    DFsList: IDataframe[];
    currentModel: IModel | null;
    tree: ISimpleDataframe[];
    modelsList: IModel[];
    predictionList: any[];
    page: number;
    currentValues: any;
    pagesCount: number;
    jobs: IJob[];
    corrMatrix: any;
}

const initialState: DataframeState = {
    DFsList: [],
    currentModel: null,
    tree: [],
    modelsList: [],
    predictionList: [],
    page: 0,
    currentValues: {},
    pagesCount: 0,
    jobs: [],
    corrMatrix: {}
};

export const dataframeSlice = createSlice({
    name: 'dataframe',
    initialState,
    reducers: {
        setDataframes: (state, action: PayloadAction<IDataframe[]>) => {
            state.DFsList = action.payload;
        },
        setCurrentModel: (state, action: PayloadAction<IModel>) => {
            state.currentModel = action.payload;
        },
        setModels: (state, action: PayloadAction<IModel[]>) => {
            state.modelsList = action.payload;
        },
        setJobs: (state, action: PayloadAction<IJob[]>) => {
            state.jobs = action.payload;
        },
        setPredictions: (state, action: PayloadAction<any[]>) => {
            state.predictionList = action.payload;
        },
        setTree: (state, action: PayloadAction<ISimpleDataframe[]>) => {
            state.tree = action.payload;
        },
        setCorrMatrix: (state, action: PayloadAction<any>) => {
            state.corrMatrix = action.payload;
        },
        setCurrentValues: (state, action: PayloadAction<any>) => {
            state.pagesCount = action.payload.total;
            state.currentValues = action.payload.records;
        },
        setTargetFeature: (state, action: PayloadAction<{ id: string, search: string | null }>) => {
            const found = state.DFsList.find((df: IDataframe) => df._id === action.payload.id);
            if (found) found.target_feature = action.payload.search;
        },
        addDataframe: (state, action: PayloadAction<IDataframe>) => {
            state.DFsList.push(action.payload);
        },
        renameDataframe: (state, action: PayloadAction<string[]>) => {
            const found = state.DFsList.find((df: IDataframe) => df.filename === action.payload[0]);
            if (found) found.filename = action.payload[1];
        },
        renameModel: (state, action: PayloadAction<string[]>) => {
            const found = state.modelsList.find((md: IModel) => md.filename === action.payload[0]);
            if (found) found.filename = action.payload[1];
        },
        updateJob: (state, action: PayloadAction<{ job_id: string, job_type: string, status: string, message: string }>) => {
            const { job_id, job_type, status, message } = action.payload;
            const found = state.jobs.find((job: IJob) => job._id === job_id);
            if (!found) return;

            found.type = job_type;
            found.status = status;
            found.output_message = message;
        },
        prevPage: (state) => {
            --state.page;
        },
        nextPage: (state) => {
            ++state.page;
        },
        setPage: (state, action: PayloadAction<number>) => {
            state.page = action.payload;
        }
    }
})

export const { setCurrentValues, setCurrentModel, setTree, renameModel, setCorrMatrix, setPredictions, setJobs, renameDataframe, setModels, updateJob, setDataframes, prevPage, nextPage, addDataframe, setPage, setTargetFeature } = dataframeSlice.actions;
export default dataframeSlice.reducer;
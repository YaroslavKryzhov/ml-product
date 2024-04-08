import { configureStore } from '@reduxjs/toolkit';

import miscReducer from '@/redux/miscSlice';
import dataframeReducer from "@/redux/dataframeSlice";
import methodApplyReducer from "@/redux/methodApplySlice";

export const store = configureStore({
    reducer: {
        misc: miscReducer,
        dataframe: dataframeReducer,
        methodApply: methodApplyReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
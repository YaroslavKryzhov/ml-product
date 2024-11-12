import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice } from '@reduxjs/toolkit';
import { IAppliedMethod, IRawMethod } from "@/utils/types";

interface MethodApplyState {
    res: IAppliedMethod[];
}

const initialState: MethodApplyState = {
    res: []
};

export const MethodApplySlice = createSlice({
    name: 'methodApply',
    initialState,
    reducers: {
        selectMethod: (state, action: PayloadAction<IRawMethod>) => {
            state.res.push({ ...action.payload, columns: [] });
        },
        deselectMethod: (state, action: PayloadAction<IRawMethod>) => {
            state.res = state.res.filter((m: IAppliedMethod) => m.method_name !== action.payload.method_name);
        },
        checkFeature: (state, action: PayloadAction<any>) => {
            const { method, feature }: { method: IRawMethod, feature: string } = action.payload;
            const foundMethod: number = state.res.findIndex((m: IAppliedMethod) => m.method_name === method.method_name);
            if (foundMethod === -1) return;

            if (!state.res[foundMethod].columns.includes(feature)) state.res[foundMethod].columns.push(feature);
            else state.res[foundMethod].columns = state.res[foundMethod].columns.filter((f: string) => f !== feature);
        }
    }
})

export const { selectMethod, deselectMethod, checkFeature } = MethodApplySlice.actions;
export default MethodApplySlice.reducer;
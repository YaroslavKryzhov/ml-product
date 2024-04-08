import type { PayloadAction } from "@reduxjs/toolkit";
import { createSlice } from '@reduxjs/toolkit';

interface MiscState {
    isLaptop: boolean;
    Authorization: string | null;
}

const initialState: MiscState = {
    isLaptop: false,
    Authorization: null
};

export const miscSlice = createSlice({
    name: 'misc',
    initialState,
    reducers: {
        setIsLaptop: (state, action: PayloadAction<boolean>) => {
            state.isLaptop = action.payload;
        },
        setToken: (state, action: PayloadAction<string>) => {
            state.Authorization = `Bearer ${action.payload}`;
        }
    }
})

export const { setIsLaptop, setToken } = miscSlice.actions;
export default miscSlice.reducer;
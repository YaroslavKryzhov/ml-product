import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit";
import { sideEffectsMiddleware } from "./middleware/sideEffects";
import authApi, { authApi as authApiSlice } from "./reducers/api/auth.api";

export const store = configureStore({
  reducer: { authApi },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }).concat([
      authApiSlice.middleware,
      sideEffectsMiddleware,
    ]),
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;

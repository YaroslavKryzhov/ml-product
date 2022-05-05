import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit";
import { sideEffectsMiddleware } from "./middleware/sideEffects";
import authApi, { authApi as authApiSlice } from "./reducers/api/auth.api";
import auth from "./reducers/auth";
import documents from "./reducers/documents";
import documentsApi, {
  documentsApi as documentsApiSlice,
} from "./reducers/api/documents.api";

import main from "./reducers/main";

export const store = configureStore({
  reducer: { authApi, main, auth, documents, documentsApi },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }).concat([
      authApiSlice.middleware,
      documentsApiSlice.middleware,
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

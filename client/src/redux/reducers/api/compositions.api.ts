import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import {
  CompositionInfo,
  Model,
  TaskResponseData,
  TaskStatus,
  TrainParamsPayload,
} from "../types";
import { entries } from "lodash";
import { store } from "ducks/store";
import { SnackBarType, addNotice } from "../notices";
import { removePendingTask } from "../documents";
import { socketManager } from "./socket";

enum Tags {
  compositions = "compositions",
  singleComposition = "singleComposition",
}

export const compositionsApi = createApi({
  reducerPath: "compositionsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: ROUTES.COMPOSITIONS.BASE,
    prepareHeaders: addAuthHeader,
  }),
  tagTypes: Object.values(Tags),
  endpoints: (builder) => ({
    compositionInfo: builder.query<CompositionInfo, { model_id: string }>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.BASE,
        params,
      }),
      providesTags: [Tags.singleComposition],
    }),
    deleteComposition: builder.mutation<string, { model_id: string }>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.BASE,
        params,
        method: "DELETE",
      }),
      invalidatesTags: [Tags.compositions],
    }),
    renameComposition: builder.mutation<
      string,
      { model_id: string; new_model_name: string }
    >({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.RENAME,
        params,
        method: "PUT",
      }),
      invalidatesTags: [Tags.compositions],
    }),
    allCompositions: builder.query<CompositionInfo[], void>({
      query: () => ({
        url: ROUTES.COMPOSITIONS.ALL,
      }),
      providesTags: [Tags.compositions],
    }),

    downloadComposition: builder.mutation<
      null,
      { model_id: string; model_name: string }
    >({
      async queryFn({ model_id, model_name }) {
        const res = await fetch(
          `${ROUTES.COMPOSITIONS.BASE}${ROUTES.COMPOSITIONS.DOWNLOAD}?model_id=${model_id}`,
          {
            headers: { Authorization: `Bearer ${localStorage.authToken}` },
          }
        );

        const blob = await res.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = model_name;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        return {
          data: null,
          meta: null,
        };
      },
    }),
    predictComposition: builder.mutation<
      { predictions: string[]; [key: string]: Array<string | number> },
      { model_id: string; dataframe_id: string }
    >({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.PREDICT,
        params,
        method: "GET",
      }),
    }),
    trainComposition: builder.mutation<
      null,
      { body: Model[]; params: TrainParamsPayload }
    >({
      async queryFn({ body, params }) {
        const res = await fetch(
          `${ROUTES.COMPOSITIONS.BASE}${ROUTES.COMPOSITIONS.TRAIN}?${entries(
            params
          )
            .map(([key, val]) => `${key}=${val}`)
            .join("&")}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.authToken}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
            method: "POST",
          }
        );

        const task = (await res.json()) as string;
        const taskId = JSON.stringify(params);

        if (!res.ok) {
          store.dispatch(
            addNotice({
              label: `Не удалось натренировать модель '${params.model_name}'`,
              type: SnackBarType.error,
              id: Date.now(),
            })
          );
          store.dispatch(removePendingTask(taskId));
        }

        socketManager.taskSubscription(task, (data: TaskResponseData) => {
          store.dispatch(removePendingTask(taskId));
          if (data.status === TaskStatus.success) {
            store.dispatch(
              addNotice({
                label: `Модель '${params.model_name}' успешно натренирована`,
                type: SnackBarType.success,
                id: Date.now(),
              })
            );

            store.dispatch(
              compositionsApi.util.invalidateTags([
                Tags.compositions,
                Tags.singleComposition,
              ])
            );
          } else {
            store.dispatch(
              addNotice({
                label: `Не удалось натренировать модель '${params.model_name}'`,
                type: SnackBarType.error,
                id: Date.now(),
              })
            );
          }
        });

        store.dispatch(
          compositionsApi.util.invalidateTags([
            Tags.compositions,
            Tags.singleComposition,
          ])
        );

        return {
          data: null,
          meta: null,
        };
      },
    }),
  }),
});

export const {
  useAllCompositionsQuery,
  useCompositionInfoQuery,
  useDeleteCompositionMutation,
  useDownloadCompositionMutation,
  usePredictCompositionMutation,
  useRenameCompositionMutation,
  useTrainCompositionMutation,
} = compositionsApi;
export default compositionsApi.reducer;

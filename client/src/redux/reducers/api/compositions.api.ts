import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import {
  CompositionInfo,
  CompositionInfoShort,
  Model,
  TrainParamsPayload,
} from "../types";

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
    compositionInfo: builder.query<CompositionInfo, { model_name: string }>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.INFO,
        params,
      }),
      providesTags: [Tags.singleComposition],
    }),
    deleteComposition: builder.mutation<string, { model_name: string }>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.BASE,
        params,
        method: "DELETE",
      }),
      invalidatesTags: [Tags.compositions],
    }),
    renameComposition: builder.mutation<
      string,
      { model_name: string; new_model_name: string }
    >({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.RENAME,
        params,
        method: "PUT",
      }),
      invalidatesTags: [Tags.compositions],
    }),
    allCompositions: builder.query<CompositionInfoShort[], void>({
      query: () => ({
        url: ROUTES.COMPOSITIONS.ALL,
      }),
      providesTags: [Tags.compositions],
    }),

    downloadComposition: builder.mutation<null, { model_name: string }>({
      async queryFn({ model_name }) {
        const res = await fetch(
          `${ROUTES.COMPOSITIONS.BASE}${ROUTES.COMPOSITIONS.DOWNLOAD}?model_name=${model_name}`,
          {
            headers: { Authorization: `Bearer ${localStorage.authToken}` },
          }
        );

        const blob = await res.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = model_name + ".pickle";
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
      { predictions: string[] },
      { model_name: string; document_name: string }
    >({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.PREDICT,
        params,
        method: "GET",
      }),
    }),
    trainComposition: builder.mutation<
      string,
      { body: Model[]; params: TrainParamsPayload }
    >({
      query: (payload) => ({
        url: ROUTES.COMPOSITIONS.TRAIN,
        params: payload.params,
        method: "POST",
        body: payload.body.map((model) => ({
          type: model.type,
          params: model.isDefaultParams ? {} : model.params,
        })),
      }),
      invalidatesTags: [Tags.compositions],
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

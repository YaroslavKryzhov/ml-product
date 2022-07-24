import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import { CompositionInfo, CompositionInfoShort } from "../types";

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
    downloadComposition: builder.mutation<string, { model_name: string }>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.DOWNLOAD,
        params,
        method: "GET",
      }),
    }),
    predictComposition: builder.query<
      string,
      { model_name: string; document_name: string }
    >({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.PREDICT,
        params,
      }),
    }),
    trainComposition: builder.mutation<string, {}>({
      query: (params) => ({
        url: ROUTES.COMPOSITIONS.TRAIN,
        params,
        method: "POST",
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
  usePredictCompositionQuery,
  useRenameCompositionMutation,
  useTrainCompositionMutation,
} = compositionsApi;
export default compositionsApi.reducer;

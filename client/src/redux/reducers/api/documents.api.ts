import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import {
  DescribeDoc,
  DFInfo,
  DocumentInfo,
  DocumentInfoShort,
  DocumentMethod,
  StandardResponse,
  FullDocument,
  TaskType,
} from "../types";

const buildFileForm = (file: File) => {
  const form = new FormData();
  form.append("file", file);

  return form;
};

enum Tags {
  documents = "documents",
  singleDocument = "singleDocument",
  columnMarks = "columnMarks",
  pipeline = "pipeline",
}

export const documentsApi = createApi({
  reducerPath: "documentsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: ROUTES.DOCUMENTS.BASE,
    prepareHeaders: addAuthHeader,
  }),
  tagTypes: Object.values(Tags),
  endpoints: (builder) => ({
    document: builder.query<FullDocument, { filename: string; page: number }>({
      query: ({ filename, page }) => ({
        url: ROUTES.DOCUMENTS.SHOW,
        params: { filename, page },
      }),
      providesTags: [Tags.singleDocument],
    }),
    postDocument: builder.mutation<
      string | StandardResponse,
      { filename: string; file: File }
    >({
      query: ({ filename, file }) => ({
        url: ROUTES.DOCUMENTS.BASE,
        params: { filename },
        method: "POST",
        body: buildFileForm(file),
      }),
      invalidatesTags: [Tags.documents],
    }),
    deleteDocument: builder.mutation<string, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.BASE,
        params: { filename },
        method: "DELETE",
      }),
      invalidatesTags: [Tags.documents],
    }),
    infoDocument: builder.query<DocumentInfo, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.INFO,
        params: { filename },
      }),
      providesTags: [Tags.singleDocument],
    }),
    infoStatsDocument: builder.query<DFInfo[], string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.DF_INFO,
        params: { filename },
      }),
      providesTags: [Tags.singleDocument],
    }),
    describeDocument: builder.query<DescribeDoc, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.DESCRIBE,
        params: { filename },
      }),
      providesTags: [Tags.singleDocument],
    }),
    pipelineDocument: builder.query<
      string,
      { document_from: string; document_to: string }
    >({
      query: ({ document_from, document_to }) => ({
        url: ROUTES.DOCUMENTS.PIPE,
        params: { document_from, document_to },
      }),
      providesTags: [Tags.pipeline],
    }),
    allDocuments: builder.query<DocumentInfoShort[], void>({
      query: () => ({
        url: ROUTES.DOCUMENTS.ALL,
      }),
      providesTags: [Tags.documents],
    }),
    downloadDocument: builder.mutation<null, string>({
      async queryFn(filename) {
        const res = await fetch(
          `${ROUTES.DOCUMENTS.BASE}${ROUTES.DOCUMENTS.DOWNLOAD}?filename=${filename}`,
          {
            headers: { Authorization: `Bearer ${localStorage.authToken}` },
          }
        );

        const blob = await res.blob();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        return {
          data: null,
          meta: null,
        };
      },
    }),
    renameDocument: builder.mutation<
      string,
      { filename: string; new_filename: string }
    >({
      query: ({ filename, new_filename }) => ({
        url: ROUTES.DOCUMENTS.RENAME,
        params: { filename, new_filename },
        method: "PUT",
      }),
      invalidatesTags: [Tags.documents],
    }),
    columnsDocument: builder.query<string[], string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.COLUMNS,
        params: { filename },
      }),
    }),
    applyDocMethod: builder.mutation<
      string,
      { filename: string; function_name: DocumentMethod }
    >({
      query: ({ filename, function_name }) => ({
        url: ROUTES.DOCUMENTS.APPLY_METHOD,
        params: { filename, function_name },
        method: "PUT",
      }),
      invalidatesTags: [Tags.pipeline, Tags.singleDocument],
    }),
    selectDocumentTarget: builder.mutation<
      void,
      { filename: string; targetColumn: string; taskType: TaskType }
    >({
      query: ({ targetColumn, filename, taskType }) => ({
        url: ROUTES.DOCUMENTS.SELECT_TARGET,
        params: { filename, target_column: targetColumn, task_type: taskType },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    copyPipeline: builder.mutation<void, { from: string; to: string }>({
      query: ({ from, to }) => ({
        url: ROUTES.DOCUMENTS.COPY_PIPELINE,
        params: { from_document: from, to_document: to },
        method: "POST",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    markAsCategorical: builder.mutation<
      void | StandardResponse,
      { filename: string; columnName: string }
    >({
      query: ({ columnName, filename }) => ({
        url: ROUTES.DOCUMENTS.MARK_CATEGORICAL,
        params: { filename, column_name: columnName },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    markAsNumeric: builder.mutation<
      void | StandardResponse,
      { filename: string; columnName: string }
    >({
      query: ({ columnName, filename }) => ({
        url: ROUTES.DOCUMENTS.MARK_NUMERIC,
        params: { filename, column_name: columnName },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    deleteColumn: builder.mutation<
      void | StandardResponse,
      { filename: string; columnName: string }
    >({
      query: ({ columnName, filename }) => ({
        url: ROUTES.DOCUMENTS.DELETE_COLUMN,
        params: { filename, column_name: columnName },
        method: "DELETE",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
  }),
});

export const {
  useAllDocumentsQuery,
  usePostDocumentMutation,
  useDeleteDocumentMutation,
  useInfoDocumentQuery,
  useRenameDocumentMutation,
  useDownloadDocumentMutation,
  useDocumentQuery,
  useColumnsDocumentQuery,
  useApplyDocMethodMutation,
  useDescribeDocumentQuery,
  useInfoStatsDocumentQuery,
  useSelectDocumentTargetMutation,
  useMarkAsCategoricalMutation,
  useMarkAsNumericMutation,
  useCopyPipelineMutation,
  useDeleteColumnMutation,
} = documentsApi;
export default documentsApi.reducer;

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { COPY_PIPELINE_ID, ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import {
  DescribeDoc,
  DFInfo,
  DocumentInfo,
  DocumentMethod,
  ErrorResponse,
  FullDocument,
  TaskResponseData,
  TaskStatus,
} from "../types";
import { socketManager } from "./socket";
import { store } from "ducks/store";
import { addNotice, SnackBarType } from "../notices";
import { MethodHeaders } from "app/Workplace/Documents/Single/DocumentMethods/constants";
import { removePendingTask } from "../documents";

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
    document: builder.query<
      FullDocument,
      { dataframe_id: string; page: number }
    >({
      query: ({ dataframe_id, page }) => ({
        url: ROUTES.DOCUMENTS.SHOW,
        params: { dataframe_id, page },
      }),
      providesTags: [Tags.singleDocument],
    }),
    postDocument: builder.mutation<
      string | ErrorResponse,
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
      query: (dataframe_id) => ({
        url: ROUTES.DOCUMENTS.BASE,
        params: { dataframe_id },
        method: "DELETE",
      }),
      invalidatesTags: [Tags.documents],
    }),
    infoDocument: builder.query<DocumentInfo, string>({
      query: (dataframe_id) => ({
        url: ROUTES.DOCUMENTS.INFO,
        params: { dataframe_id },
      }),
      providesTags: [Tags.singleDocument],
    }),
    infoStatsDocument: builder.query<DFInfo[], string>({
      query: (dataframe_id) => ({
        url: ROUTES.DOCUMENTS.DF_INFO,
        params: { dataframe_id },
      }),
      providesTags: [Tags.singleDocument],
    }),
    describeDocument: builder.query<DescribeDoc, string>({
      query: (dataframe_id) => ({
        url: ROUTES.DOCUMENTS.DESCRIBE,
        params: { dataframe_id },
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
    allDocuments: builder.query<DocumentInfo[], void>({
      query: () => ({
        url: ROUTES.DOCUMENTS.ALL,
      }),
      providesTags: [Tags.documents],
    }),
    downloadDocument: builder.mutation<
      null,
      { dataframe_id: string; filename: string }
    >({
      async queryFn({ dataframe_id, filename }) {
        const res = await fetch(
          `${ROUTES.DOCUMENTS.BASE}${ROUTES.DOCUMENTS.DOWNLOAD}?dataframe_id=${dataframe_id}`,
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
      { dataframe_id: string; new_filename: string }
    >({
      query: ({ dataframe_id, new_filename }) => ({
        url: ROUTES.DOCUMENTS.RENAME,
        params: { dataframe_id, new_filename },
        method: "PUT",
      }),
      invalidatesTags: [Tags.documents, Tags.singleDocument],
    }),
    columnsDocument: builder.query<string[], string>({
      query: (dataframe_id) => ({
        url: ROUTES.DOCUMENTS.COLUMNS,
        params: { dataframe_id },
      }),
      providesTags: [Tags.singleDocument],
    }),
    applyDocMethod: builder.mutation<
      null,
      { dataframe_id: string; function_name: DocumentMethod }
    >({
      async queryFn({ dataframe_id, function_name }) {
        const res = await fetch(
          `${ROUTES.DOCUMENTS.BASE}${ROUTES.DOCUMENTS.APPLY_METHOD}?dataframe_id=${dataframe_id}&function_name=${function_name}`,
          {
            headers: { Authorization: `Bearer ${localStorage.authToken}` },
            method: "POST",
          }
        );

        const task = (await res.json()) as string;
        const methodLabel = MethodHeaders.find(
          (x) => x.value === function_name
        )?.label;

        if (!res.ok) {
          store.dispatch(
            addNotice({
              label: `Метод '${methodLabel}' не выполнен. Ошибка запроса. ${
                res.statusText || ""
              }`,
              type: SnackBarType.error,
              id: Date.now(),
            })
          );
          store.dispatch(removePendingTask(function_name));
        }

        socketManager.taskSubscription(task, (data: TaskResponseData) => {
          store.dispatch(removePendingTask(function_name));
          if (data.status === TaskStatus.success) {
            store.dispatch(
              addNotice({
                label: `Метод '${methodLabel}' успешно выполнен`,
                type: SnackBarType.success,
                id: Date.now(),
              })
            );

            store.dispatch(
              documentsApi.util.invalidateTags([
                Tags.singleDocument,
                Tags.pipeline,
              ])
            );
          } else {
            store.dispatch(
              addNotice({
                label: `Метод '${methodLabel}' не выполнен. Ошибка. ${data.message}`,
                type: SnackBarType.error,
                id: Date.now(),
              })
            );
          }
        });

        return {
          data: null,
          meta: null,
        };
      },
    }),
    selectDocumentTarget: builder.mutation<
      void,
      { dataframe_id: string; target_column: string }
    >({
      query: ({ target_column, dataframe_id }) => ({
        url: ROUTES.DOCUMENTS.SELECT_TARGET,
        params: { dataframe_id, target_column },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    copyPipeline: builder.mutation<
      null,
      { dataframe_id_from: string; dataframe_id_to: string }
    >({
      async queryFn({ dataframe_id_to, dataframe_id_from }) {
        const res = await fetch(
          `${ROUTES.DOCUMENTS.BASE}${ROUTES.DOCUMENTS.COPY_PIPELINE}?dataframe_id_from=${dataframe_id_from}&dataframe_id_to=${dataframe_id_to}`,
          {
            headers: { Authorization: `Bearer ${localStorage.authToken}` },
            method: "POST",
          }
        );

        const task = (await res.json()) as string;

        if (!res.ok) {
          store.dispatch(
            addNotice({
              label: `Копирование пайплайна не выполнено. Ошибка запроса. ${
                res.statusText || ""
              }`,
              type: SnackBarType.error,
              id: Date.now(),
            })
          );
          store.dispatch(removePendingTask(COPY_PIPELINE_ID));
        }

        socketManager.taskSubscription(task, (data: TaskResponseData) => {
          store.dispatch(removePendingTask(COPY_PIPELINE_ID));
          if (data.status === TaskStatus.success) {
            store.dispatch(
              addNotice({
                label: `Копирование пайплайна успешно выполнено`,
                type: SnackBarType.success,
                id: Date.now(),
              })
            );
            store.dispatch(
              documentsApi.util.invalidateTags([
                Tags.singleDocument,
                Tags.pipeline,
              ])
            );
          } else {
            store.dispatch(
              addNotice({
                label: `Копирование пайплайна не выполнено. Ошибка. ${data.message}`,
                type: SnackBarType.error,
                id: Date.now(),
              })
            );
          }
        });

        return {
          data: null,
          meta: null,
        };
      },
    }),
    markAsCategorical: builder.mutation<
      void | ErrorResponse,
      { dataframe_id: string; column_name: string }
    >({
      query: ({ dataframe_id, column_name }) => ({
        url: ROUTES.DOCUMENTS.MARK_CATEGORICAL,
        params: { dataframe_id, column_name },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    markAsNumeric: builder.mutation<
      void | ErrorResponse,
      { dataframe_id: string; column_name: string }
    >({
      query: ({ column_name, dataframe_id }) => ({
        url: ROUTES.DOCUMENTS.MARK_NUMERIC,
        params: { dataframe_id, column_name },
        method: "PUT",
      }),
      invalidatesTags: [Tags.singleDocument],
    }),
    deleteColumn: builder.mutation<
      void | ErrorResponse,
      { dataframe_id: string; column_name: string }
    >({
      query: ({ column_name, dataframe_id }) => ({
        url: ROUTES.DOCUMENTS.DELETE_COLUMN,
        params: { dataframe_id, column_name },
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

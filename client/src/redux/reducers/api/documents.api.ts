import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import { ColumnMarksPayload, DocumentInfo, DocumentInfoShort } from "../types";

const buildFileForm = (file: File) => {
  const form = new FormData();
  form.append("file", file);

  return form;
};

enum Tags {
  documents = "documents",
}

export const documentsApi = createApi({
  reducerPath: "documentsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: ROUTES.DOCUMENTS.BASE,
    prepareHeaders: addAuthHeader,
  }),
  tagTypes: [Tags.documents],
  endpoints: (builder) => ({
    document: builder.query<Document, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.BASE,
        params: { filename },
      }),
      // TODO: weird back string response. Need to be rewrited to JSON
      transformResponse: (response: string) => JSON.parse(response),
    }),
    postDocument: builder.mutation<string, { filename: string; file: File }>({
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
    }),
    pipelineDocument: builder.query<
      string,
      { document_from: string; document_to: string }
    >({
      query: ({ document_from, document_to }) => ({
        url: ROUTES.DOCUMENTS.PIPE,
        params: { document_from, document_to },
      }),
    }),
    allDocuments: builder.query<DocumentInfoShort[], void>({
      query: () => ({
        url: ROUTES.DOCUMENTS.ALL,
      }),
      providesTags: [Tags.documents],
    }),
    downloadDocument: builder.query<string, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.DOWNLOAD,
        params: { filename },
      }),
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
    }),
    columnsDocument: builder.query<string, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.COLUMNS,
        params: { filename },
      }),
    }),

    columnMarksDocument: builder.query<string, string>({
      query: (filename) => ({
        url: ROUTES.DOCUMENTS.COLUMN_MARKS,
        params: { filename },
      }),
    }),
    changeColumnMarks: builder.mutation<
      string,
      { filename: string; body: ColumnMarksPayload }
    >({
      query: ({ filename, body }) => ({
        url: ROUTES.DOCUMENTS.COLUMN_MARKS,
        params: { filename },
        body,
        method: "PUT",
      }),
    }),
  }),
});

export const {
  useAllDocumentsQuery,
  usePostDocumentMutation,
  useDeleteDocumentMutation,
} = documentsApi;
export default documentsApi.reducer;

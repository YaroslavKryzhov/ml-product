import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ROUTES } from "../../constants";
import { addAuthHeader } from "./helpers";
import { AuthPayload, EmittedToken, RegisterPayload } from "../types";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: ROUTES.AUTH.BASE,
    prepareHeaders: addAuthHeader,
  }),
  endpoints: (builder) => ({
    auth: builder.mutation<EmittedToken, AuthPayload>({
      query: (body) => ({
        url: ROUTES.AUTH.LOGIN,
        method: "POST",
        body,
      }),
      async onQueryStarted(_, { queryFulfilled }) {
        try {
          const token = await queryFulfilled;
          localStorage.authToken = token.data.access_token;
        } catch {
          localStorage.authToken = "";
        }
      },
    }),
    register: builder.mutation<EmittedToken, RegisterPayload>({
      query: (body) => ({
        url: ROUTES.AUTH.REGISTER,
        method: "POST",
        body,
      }),
    }),
  }),
});

export const { useAuthMutation, useRegisterMutation } = authApi;
export default authApi.reducer;

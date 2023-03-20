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
      query: (data) => ({
        url: ROUTES.AUTH.LOGIN,
        method: "POST",
        body: new URLSearchParams({
          username: data.username,
          password: data.password,
        }),
      }),
    }),
    centrifugoSocket: builder.query<string, void>({
      query: () => ({
        url: ROUTES.AUTH.CENTRIFUGO,
      }),
    }),
    // TODO: unsafe register, rework after back ready
    register: builder.mutation<EmittedToken, RegisterPayload>({
      query: (body) => ({
        url: ROUTES.AUTH.REGISTER,
        method: "POST",
        body: {
          ...body,
          is_active: true,
          is_superuser: false,
          is_verified: false,
        },
      }),
    }),
  }),
});

export const {
  useAuthMutation,
  useRegisterMutation,
  useCentrifugoSocketQuery,
} = authApi;
export default authApi.reducer;

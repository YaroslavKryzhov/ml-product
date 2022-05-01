export type AuthPayload = {};

export type RegisterPayload = {};

export type EmittedToken = {
  access_token: string;
  token_type: string;
};

export enum AuthPage {
  auth = "auth",
  register = "register",
}

export type AuthSlice = {
  page: AuthPage;
  passwordInput: string;
  secondPasswordInput: string;
  emailInput: string;
};

export type DecodedToken = {
  user_id: string;
  exp: number;
};

export enum AppPage {
  Authentication = "Authentication",
}

export type MainSlice = {
  page: AppPage;
};

declare global {
  interface Window {
    localStorage: { authToken: string };
  }
}

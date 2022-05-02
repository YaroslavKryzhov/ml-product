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

export enum WorkPage {
  Documents = "Documents",
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
  Workplace = "Workplace",
}

export type MainSlice = {
  page: AppPage;
  isBlockingLoader: boolean;
};

declare global {
  interface Window {
    localStorage: { authToken: string };
  }
}

export type DocumentsSlice = {};

export type Document = {
  [key: string]: string[] | number[];
};

export type DocumentInfo = {
  id: string;
  name: string;
  upload_date: string;
  change_date: string;
  pipeline: string[];
  column_marks: {
    numeric: string[];
    categorical: string[];
    target: string;
  };
};

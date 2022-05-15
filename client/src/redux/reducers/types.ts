export enum AuthPage {
  auth = "auth",
  register = "register",
}

export enum AppPage {
  Authentication = "authentication",
  Workplace = "workplace",
}

export enum WorkPage {
  Documents = "documents",
}

export enum DocumentPage {
  List = "list",
  Single = "single",
}

export type AuthSlice = {
  passwordInput: string;
  secondPasswordInput: string;
  emailInput: string;
};

export type MainSlice = {
  isBlockingLoader: boolean;
};

export type DecodedToken = {
  user_id: string;
  exp: number;
};

export type AuthPayload = { username: string; password: string };

export type RegisterPayload = {};

export type EmittedToken = {
  access_token: string;
  token_type: string;
};

declare global {
  interface Window {
    localStorage: { authToken: string };
  }
}

export type Document = {
  [key: string]: string[] | number[];
};

export type DocumentInfo = DocumentInfoShort & {
  id: string;
  pipeline: string[];
  column_marks: {
    numeric: string[];
    categorical: string[];
    target: string;
  };
};

export type DocumentInfoShort = {
  name: string;
  upload_date: string;
  change_date: string;
};

export enum CategoryMark {
  numeric = "numeric",
  categorical = "categorical",
  target = "target",
}

export type ColumnMarksPayload = {
  [CategoryMark.numeric]: string[];
  [CategoryMark.categorical]: string[];
  [CategoryMark.target]: string;
};

export type FullDocument = { [key: string]: (string | number)[] };

export enum DocumentMethod {
  removeDuplicates = "remove_duplicates",
  dropNa = "drop_na",
  missInsertMeanMode = "miss_insert_mean_mode",
  missLinearImputer = "miss_linear_imputer",
  standartizeFeatures = "standartize_features",
  ordinalEncoding = "ordinal_encoding",
  oneHotEncoding = "one_hot_encoding",
  outliersIsolationForest = "outliers_isolation_forest",
  outliersEllipticEnvelope = "outliers_elliptic_envelope",
  outliersLocalFactor = "outliers_local_factor",
  outliersOneClassSvm = "outliers_one_class_svm",
}

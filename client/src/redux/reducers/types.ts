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
  Compositions = "compositions",
}

export enum DocumentPage {
  List = "list",
  Single = "single",
}

export enum CompositionPage {
  List = "CompositionList",
  Single = "CompositionSingle",
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

export type PipelineUnit = { function_name: string; param: string | null };

export type DocumentInfo = DocumentInfoShort & {
  id: string;
  pipeline: PipelineUnit[];
  column_marks: {
    numeric: string[];
    categorical: string[];
    target: string;
  };
};

export type DocumentStatsColumnInfo = {
  type: CategoryMark;
  data: Record<string, number>;
};

export type DocumentStatsInfo = {
  column_name: string[];
  data_type: string[];
  non_null_count: string[];
};

export type DescribeDoc = {
  [key: string]: { [key: string]: number };
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

export type NumericData = { value: number; left: number; right: number };
export type CategoricalData = { name: string; value: number };

export type ColumnStats = {
  name: string;
  type: CategoryMark;
  data: (NumericData | CategoricalData)[];
};

export type ColumnMarksPayload = {
  [CategoryMark.numeric]: string[];
  [CategoryMark.categorical]: string[];
  [CategoryMark.target]: string;
};

export type FullDocument = {
  total: number;
  records: Record<string, string | number>;
};

export enum DocumentMethod {
  removeDuplicates = "remove_duplicates",
  dropNa = "drop_na",
  missInsertMeanMode = "miss_insert_mean_mode",
  missLinearImputer = "miss_linear_imputer",
  standardize_features = "standardize_features",
  ordinalEncoding = "ordinal_encoding",
  oneHotEncoding = "one_hot_encoding",
  outliersIsolationForest = "outliers_isolation_forest",
  outliersEllipticEnvelope = "outliers_elliptic_envelope",
  outliersLocalFactor = "outliers_local_factor",
  outliersOneClassSvm = "outliers_one_class_svm",
}

export enum PandasInfoColumns {
  columnName = "column_name",
  dataType = "data_type",
  nonNullCount = "non_null_count",
}

export enum TaskType {
  regression = "regression",
  classification = "classification",
}

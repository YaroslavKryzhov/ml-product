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
  List = "list",
  Single = "single",
  Create = "create",
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
  column_types: {
    numeric: string[];
    categorical: string[];
    target: string;
    task_type: TaskType;
  };
};

export type DFInfo = {
  type: CategoryMark;
  data: (NumericData | CategoricalData)[];
  name: string;
  not_null_count: number;
  data_type: string;
};

export type DescribeDoc = {
  [key: string]: { [key: string]: number };
};

export type DocumentInfoShort = {
  name: string;
  upload_date: string;
  change_date: string;
  pipeline: PipelineUnit[];
};

export enum CategoryMark {
  numeric = "numeric",
  categorical = "categorical",
  target = "target",
}

export type NumericData = { value: number; left: number; right: number };
export type CategoricalData = { name: string; value: number };

export type FullDocument = {
  total: number;
  records: Record<string, string | number>;
};

export enum DocumentMethod {
  removeDuplicates = "remove_duplicates",
  dropNa = "drop_na",
  missInsertMeanMode = "miss_insert_mean_mode",
  missLinearImputer = "miss_linear_imputer",
  missKnnImputer = "miss_knn_imputer",
  standardize_features = "standardize_features",
  ordinalEncoding = "ordinal_encoding",
  oneHotEncoding = "one_hot_encoding",
  outliersIsolationForest = "outliers_isolation_forest",
  outliersEllipticEnvelope = "outliers_elliptic_envelope",
  outliersLocalFactor = "outliers_local_factor",
  outliersOneClassSvm = "outliers_one_class_svm",
  fsSelectPercentile = "fs_select_percentile",
  fsSelectKBest = "fs_select_k_best",
  fsSelectFpr = "fs_select_fpr",
  fsSelectFdr = "fs_select_fdr",
  fsSelectFwe = "fs_select_fwe",
  fsSelectRfe = "fs_select_rfe",
  fsSelectFromModel = "fs_select_from_model",
  fsSelectPca = "fs_select_pca",
  dropСolumn = "drop_column",
}

export enum DFInfoColumns {
  columnName = "name",
  dataType = "data_type",
  nonNullCount = "not_null_count",
  type = "type",
  data = "data",
}

export enum TaskType {
  regression = "regression",
  classification = "classification",
}

export enum CompositionType {
  none = "none",
  simpleVoting = "simple_voting",
  weightedVoting = "weighted_voting",
  stacking = "stacking",
}

export enum CompositionStatus {
  training = "Training",
  trained = "Trained",
}

export enum ParamsCompositionType {
  auto = "auto",
  custom = "custom",
  default = "default",
}

export type ModelParams =
  | SGDClassifierParameters
  | ExtraTreesClassifierParameters
  | BaggingClassifierParameters
  | GradientBoostingClassifierParameters
  | AdaBoostClassifierParameters
  | RandomForestClassifierParameters
  | DecisionTreeClassifierParameters
  | null;

export type Model = {
  type: ModelTypes | null;
  params: ModelParams;
  isDefaultParams?: boolean;
};

export enum ModelTypes {
  DecisionTreeClassifier = "DecisionTreeClassifier",
  RandomForestClassifier = "RandomForestClassifier",
  // CatBoostClassifier = "CatBoostClassifier",
  AdaBoostClassifier = "AdaBoostClassifier",
  GradientBoostingClassifier = "GradientBoostingClassifier",
  BaggingClassifier = "BaggingClassifier",
  ExtraTreesClassifier = "ExtraTreesClassifier",
  SGDClassifier = "SGDClassifier",
  LinearSVC = "LinearSVC",
  SVC = "SVC",
  LogisticRegression = "LogisticRegression",
  Perceptron = "Perceptron",
  // XGBoost = "XGBoost",
  // LightGBM = "LightGBM",
}

export enum DesicionCriterion {
  gini = "gini",
  entropy = "entropy",
}

export enum DescicionSplitter {
  best = "best",
  random = "random",
}

export enum DesicionMaxFeatures {
  auto = "auto",
  sqrt = "sqrt",
  log2 = "log2",
}

export enum DesicionClassWeight {
  balanced = "balanced",
}

export enum AdaBoostAlgorithm {
  samme = "SAMME",
  sammer = "SAMME.R",
}

export enum GradientBoostingCriterion {
  friedmanMse = "friedman_mse",
  squaredError = "squared_error",
  mse = "mse",
  mae = "mae",
}

export enum GradientBoostingLoss {
  logLoss = "log_loss",
  deviance = "deviance",
  exponential = "exponential",
}

export enum SGDClassifierLoss {
  hinge = "hinge",
  log = "log",
  modifiedHuber = "modified_huber",
  squaredHinge = "squared_hinge",
  perceptron = "perceptron",
  squaredError = "squared_error",
  huber = "huber",
  epsilonInsensitive = "epsilon_insensitive",
  squaredEpsilonInsensitive = "squared_epsilon_insensitive",
}

export enum SGDClassifierLearningRate {
  constant = "constant",
  optimal = "optimal",
  invscaling = "invscaling",
  adaptive = "adaptive",
}

export enum SGDClassifierPenalty {
  l2 = "l2",
  l1 = "l1",
  elasticnet = "elasticnet",
}

export type DecisionTreeClassifierParameters = {
  criterion?: DesicionCriterion;
  splitter?: DescicionSplitter;
  max_depth?: number | null;
  min_samples_split?: number;
  min_samples_leaf?: number;
  // max_features?: DesicionMaxFeatures | string | null;
  // random_state?: number | null;
  // max_leaf_nodes?: number | null;
  // min_impurity_decrease?: number;
  // class_weight?: DesicionClassWeight | Record<string, string> | null;
  // ccp_alpha?: number;
};

export type RandomForestClassifierParameters = {
  criterion?: DesicionCriterion;
  splitter?: DescicionSplitter;
  max_depth?: number | null;
  min_samples_split?: number;
  min_samples_leaf?: number;
  bootstrap: boolean;
};

export type AdaBoostClassifierParameters = {
  n_estimators: number;
  learning_rate: number;
  algorithm: AdaBoostAlgorithm;
};

export type GradientBoostingClassifierParameters = {
  loss: GradientBoostingLoss;
  learning_rate: number;
  n_estimators: number;
  subsample: number;
  criterion: GradientBoostingCriterion;
  min_samples_split: number;
  max_depth: number;
};

export type BaggingClassifierParameters = {
  n_estimators: number;
  max_samples: number;
  max_features: number;
  bootstrap: boolean;
  bootstrap_features: boolean;
};

export type ExtraTreesClassifierParameters = {
  n_estimators: number;
  criterion?: DesicionCriterion;
  max_depth?: number | null;
  min_samples_split?: number;
  min_samples_leaf?: number;
  bootstrap: boolean;
};

export type SGDClassifierParameters = {
  loss: SGDClassifierLoss;
  penalty: SGDClassifierPenalty;
  alpha: number;
  l1_ratio: number;
  fit_intercept: boolean;
  max_iter: number;
  shuffle: boolean;
  epsilon: number;
  learning_rate: SGDClassifierLearningRate;
};

export type StandardResponse = {
  status_code: number;
  content: string;
};

export type StandardResponseData = {
  data: StandardResponse;
};

export type CompositionInfo = {
  id: string;
  name: string;
  csv_id: string;
  features: string[];
  target: string;
  create_date: string;
  task_type: TaskType;
  composition_type: CompositionType;
  composition_params: {
    type: ModelTypes;
    params: DecisionTreeClassifierParameters | RandomForestClassifierParameters;
  }[];
  stage: CompositionStatus;
  report: {
    csv_name: string;
    metrics: {
      accuracy: number;
      recall: number;
      precision: number;
      f1: number;
      roc_auc: number;
      fpr: number[];
      tpr: number[];
      roc_auc_weighted: null;
      roc_auc_micro: null;
      roc_auc_macro: null;
      fpr_micro: null;
      tpr_micro: null;
      fpr_macro: null;
      tpr_macro: null;
    };
  };
  csv_name: "Iris-binary.csv";
};

export type CompositionInfoShort = {
  name: string;
  csv_id: string;
  features: string[];
  target: string;
  create_date: string;
  task_type: TaskType;
  composition_type: CompositionType;
  stage: CompositionStatus;
};

export type TrainParamsPayload = {
  composition_type: CompositionType;
  params_type: ParamsCompositionType;
  document_name: string;
  model_name: string;
  test_size: number;
};

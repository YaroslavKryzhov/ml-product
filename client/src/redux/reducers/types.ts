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

export type DocumentInfo = {
  id: string;
  filename: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  pipeline: PipelineUnit[];
  column_types: {
    numeric: string[];
    categorical: string[];
    target: string;
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

export enum CategoryMark {
  numeric = "numeric",
  categorical = "categorical",
  target = "target",
}

export type NumericData = { value: number; left: number; right: number };
export type CategoricalData = { name: string; value: number };

export type FullDocument = {
  total: number;
  records: Record<string, (string | number)[]>;
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
  | KNeighborsClassifierParameters
  | MLPClassifierParameters
  | LogisticRegressionParameters
  | SVCParameters
  | LinearSVCParameters
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
  KNeighborsClassifier = "KNeighborsClassifier",
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

export enum LinearSVCPenalty {
  l2 = "l2",
  l1 = "l1",
}

export enum LinearSVCLoss {
  hinge = "hinge",
  squaredHinge = "squared_hinge",
}

export enum LinearSVCMultiClass {
  ovr = "ovr",
  crammer_singer = "crammer_singer",
}

export enum SVCKernel {
  linear = "linear",
  poly = "poly",
  rbf = "rbf",
  sigmoid = "sigmoid",

  precomputed = "precomputed",
}

export enum SVCGamma {
  scale = "scale",
  auto = "auto",
}

export enum LogisticRegressionPenalty {
  l1 = "l1",
  l2 = "l2",
  elasticnet = "elasticnet",
  none = "none",
}

export enum LogisticRegressionSolver {
  newtonCg = "newton-cg",
  lbfgs = "lbfgs",
  liblinear = "liblinear",
  sag = "sag",
  saga = "saga",
}

export enum MLPClassifierActivation {
  identity = "identity",
  logistic = "logistic",
  tanh = "tanh",
  relu = "relu",
}

export enum MLPClassifierSolver {
  lbfgs = "lbfgs",
  sgd = "sgd",
  adam = "adam",
}

export enum MLPClassifierLearningRate {
  constant = "constant",
  invscaling = "invscaling",
  adaptive = "adaptive",
}

export enum KNeighborsWeights {
  uniform = "uniform",
  distance = "distance",
}

export enum KNeighborsAlgorithm {
  auto = "auto",
  ball_tree = "ball_tree",
  kd_tree = "kd_tree",
  brute = "brute",
}

export enum KNeighborsMetric {
  cityblock = "cityblock",
  cosine = "cosine",
  euclidean = "euclidean",
  haversine = "haversine",
  l1 = "l1",
  l2 = "l2",
  manhattan = "manhattan",
  nan_euclidean = "nan_euclidean",
  minkowski = "minkowski",
  mahalanobis = "mahalanobis",
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

export type LinearSVCParameters = {
  penalty: LinearSVCPenalty;
  loss: LinearSVCLoss;
  dual: boolean;
  C: number;
  multi_class: LinearSVCMultiClass;
  fit_intercept: boolean;
  max_iter: number;
};

export type SVCParameters = {
  C: number;
  kernel: SVCKernel;
  degree: number;
  gamma: SVCGamma | number;
  coef0: number;
  shrinking: boolean;
  max_iter: number;
};

export type LogisticRegressionParameters = {
  penalty: LogisticRegressionPenalty;
  dual: boolean;
  C: number;
  fit_intercept: boolean;
  solver: LogisticRegressionSolver;
  max_iter: number;
  l1_ratio?: number | null;
};

export type MLPClassifierParameters = {
  hidden_layer_sizes: number[];
  activation: MLPClassifierActivation;
  solver: MLPClassifierSolver;
  alpha: number;
  max_iter: number;
  learning_rate: MLPClassifierLearningRate;
};

export type KNeighborsClassifierParameters = {
  n_neighbors: number;
  weights: KNeighborsWeights;
  algorithm: KNeighborsAlgorithm;
  metric: KNeighborsMetric;
};

export type ErrorResponse = {
  detail: string;
};

export type CompositionInfo = {
  id: string;
  filename: string;
  csv_id: string;
  features: string[];
  target: string;
  create_date: string;
  task_type: TaskType;
  composition_type: CompositionType;
  test_size: number;
  params_type: ParamsCompositionType;
  composition_params: {
    type: ModelTypes;
    params: DecisionTreeClassifierParameters | RandomForestClassifierParameters;
  }[];
  stage: CompositionStatus;
  report: {
    accuracy: number;
    recall: number;
    precision: number;
    f1: number;
    roc_auc: number;
    fpr: null | number[];
    tpr: null | number[];
    roc_auc_weighted: null;
    roc_auc_micro: null;
    roc_auc_macro: null;
    fpr_micro: number[] | null;
    tpr_micro: number[] | null;
    fpr_macro: number[] | null;
    tpr_macro: number[] | null;
  };
  csv_name: string;
};

export type TrainParamsPayload = {
  composition_type: CompositionType;
  params_type: ParamsCompositionType;
  dataframe_id: string;
  task_type: TaskType;
  model_name: string;
  test_size: number;
};

export type TaskObservePayload = {
  task_id: string;
  jwt_token: string;
};

export enum TaskStatus {
  success = "SUCCESS",
  failure = "FAILURE",
}

export type TaskResponseData = {
  task_id: string;
  status: TaskStatus;
  message: string;
};

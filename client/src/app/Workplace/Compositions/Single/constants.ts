import {
  AdaBoostAlgorithm,
  DescicionSplitter,
  DesicionCriterion,
  GradientBoostingCriterion,
  GradientBoostingLoss,
  LinearSVCLoss,
  LinearSVCMultiClass,
  LinearSVCPenalty,
  LogisticRegressionPenalty,
  LogisticRegressionSolver,
  MLPClassifierActivation,
  MLPClassifierLearningRate,
  MLPClassifierSolver,
  ModelParams,
  ModelTypes,
  SGDClassifierLearningRate,
  SGDClassifierLoss,
  SGDClassifierPenalty,
  SVCGamma,
  SVCKernel,
} from "ducks/reducers/types";

export const SELECTORS_WIDTH = "190px";

export const DTC_DEFAULT_PARAMS = {
  criterion: DesicionCriterion.gini,
  splitter: DescicionSplitter.best,
  min_samples_split: 2,
  min_samples_leaf: 1,
  // min_impurity_decrease: 0,
  // ccp_alpha: 0,
};

export const RTC_DEFAULT_PARAMS = {
  criterion: DesicionCriterion.gini,
  splitter: DescicionSplitter.best,
  min_samples_split: 2,
  min_samples_leaf: 1,
  bootstrap: true,
};

export const ADB_DEFAULT_PARAMS = {
  n_estimators: 50,
  learning_rate: 1,
  algorithm: AdaBoostAlgorithm.sammer,
};

export const GB_DEFAULT_PARAMS = {
  loss: GradientBoostingLoss.deviance,
  learning_rate: 0.1,
  n_estimators: 100,
  subsample: 1,
  criterion: GradientBoostingCriterion.friedmanMse,
  min_samples_split: 2,
  max_depth: 3,
};

export const BAGGING_DEFAULT_PARAMS = {
  n_estimators: 10,
  max_samples: 1,
  max_features: 1,
  bootstrap: true,
  bootstrap_features: false,
};

export const ETC_DEFAULT_PARAMS = {
  n_estimators: 100,
  criterion: DesicionCriterion.gini,
  min_samples_split: 2,
  min_samples_leaf: 1,
  bootstrap: true,
};

export const SDG_DEFAULT_PARAMS = {
  loss: SGDClassifierLoss.hinge,
  penalty: SGDClassifierPenalty.l2,
  alpha: 0.0001,
  l1_ratio: 0.15,
  fit_intercept: true,
  max_iter: 1000,
  shuffle: true,
  epsilon: 0.1,
  learning_rate: SGDClassifierLearningRate.optimal,
};

export const LSVC_DEFAULT_PARAMS = {
  loss: LinearSVCLoss.squaredHinge,
  penalty: LinearSVCPenalty.l2,
  dual: true,
  C: 1.0,
  multi_class: LinearSVCMultiClass.ovr,
  fit_intercept: true,
  max_iter: 1000,
};

export const SVC_DEFAULT_PARAMS = {
  C: 1.0,
  kernel: SVCKernel.rbf,
  degree: 3,
  gamma: SVCGamma.scale,
  coef0: 0.0,
  shrinking: true,
  max_iter: -1,
};

export const LR_DEFAULT_PARAMS = {
  penalty: LogisticRegressionPenalty.l2,
  dual: false,
  C: 1.0,
  fit_intercept: true,
  solver: LogisticRegressionSolver.lbfgs,
  max_iter: 100,
  l1_ratio: null,
};

export const MLP_DEFAULT_PARAMS = {
  hidden_layer_sizes: [100],
  activation: MLPClassifierActivation.relu,
  solver: MLPClassifierSolver.adam,
  alpha: 0.0001,
  max_iter: 200,
  learning_rate: MLPClassifierLearningRate.constant,
};

export const DefaultParamsModels: Partial<Record<ModelTypes, ModelParams>> = {
  [ModelTypes.DecisionTreeClassifier]: DTC_DEFAULT_PARAMS,
  [ModelTypes.RandomForestClassifier]: RTC_DEFAULT_PARAMS,
  [ModelTypes.AdaBoostClassifier]: ADB_DEFAULT_PARAMS,
  [ModelTypes.GradientBoostingClassifier]: GB_DEFAULT_PARAMS,
  [ModelTypes.BaggingClassifier]: BAGGING_DEFAULT_PARAMS,
  [ModelTypes.ExtraTreesClassifier]: ETC_DEFAULT_PARAMS,
  [ModelTypes.SGDClassifier]: SDG_DEFAULT_PARAMS,
  [ModelTypes.LinearSVC]: LSVC_DEFAULT_PARAMS,
  [ModelTypes.SVC]: SVC_DEFAULT_PARAMS,
  [ModelTypes.LogisticRegression]: LR_DEFAULT_PARAMS,
  [ModelTypes.Perceptron]: MLP_DEFAULT_PARAMS,
};

export const FloatRegexp = /^([+-]?([0-9]*[.])?[0-9]+[.]?)?$/g;

export const MIN_SAMPLES_SPLIT = 2;
export const MIN_SAMPLES_LEAF = 1;

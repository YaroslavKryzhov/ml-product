import {
  DescicionSplitter,
  DesicionClassWeight,
  DesicionCriterion,
  DesicionMaxFeatures,
  ModelParams,
  ModelTypes,
} from "ducks/reducers/types";

export const SELECTORS_WIDTH = "190px";

export const DTC_DEFAULT_PARAMS = {
  criterion: DesicionCriterion.entropy,
  splitter: DescicionSplitter.best,
  max_depth: 1,
  min_samples_split: 2,
  min_samples_leaf: 1,
  max_features: DesicionMaxFeatures.auto,
  random_state: 0,
  max_leaf_nodes: 1,
  min_impurity_decrease: 0,
  class_weight: DesicionClassWeight.balanced,
  ccp_alpha: 0,
};

export const DefaultParamsModels: Partial<Record<ModelTypes, ModelParams>> = {
  [ModelTypes.DecisionTreeClassifier]: DTC_DEFAULT_PARAMS,
};

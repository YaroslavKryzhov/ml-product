import {
  DescicionSplitter,
  DesicionCriterion,
  ModelParams,
  ModelTypes,
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

export const DefaultParamsModels: Partial<Record<ModelTypes, ModelParams>> = {
  [ModelTypes.DecisionTreeClassifier]: DTC_DEFAULT_PARAMS,
  [ModelTypes.RandomForestClassifier]: RTC_DEFAULT_PARAMS,
};

export const FloatRegexp = /^([+-]?([0-9]*[.])?[0-9]+[.]?)?$/g;

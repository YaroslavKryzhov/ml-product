import { DocumentMethod } from "ducks/reducers/types";
import { values } from "lodash";
import { BtnGroups } from "./types";

export const ButtonsGroupsLabels = {
  [BtnGroups.group1]: "Обработка данных",
  [BtnGroups.group2]: "Трансформация признаков",
  [BtnGroups.group3]: "Удаление выбросов",
  [BtnGroups.group4]: "Отбор признаков",
};

export const ButtonsData = {
  [BtnGroups.group1]: [
    { value: DocumentMethod.removeDuplicates, label: "Удаление дубликатов" },
    { value: DocumentMethod.dropNa, label: "Удаление пропусков" },
    {
      value: DocumentMethod.missInsertMeanMode,
      label: "Замена пропусков: Среднее и мода",
    },
    {
      value: DocumentMethod.missLinearImputer,
      label: "Замена пропусков: Линейная модель",
    },
    {
      value: DocumentMethod.missKnnImputer,
      label: "Замена пропусков: К-ближних соседей",
    },
  ],
  [BtnGroups.group2]: [
    {
      value: DocumentMethod.standardize_features,
      label: "Стандартизация численных признаков",
    },
    {
      value: DocumentMethod.ordinalEncoding,
      label: "Порядковое кодирование",
    },
    {
      value: DocumentMethod.oneHotEncoding,
      label: "One-Hot кодирование (OHE)",
    },
  ],
  [BtnGroups.group3]: [
    {
      value: DocumentMethod.outliersIsolationForest,
      label: "Isolation Forest",
    },
    {
      value: DocumentMethod.outliersEllipticEnvelope,
      label: "Elliptic Envelope",
    },
    {
      value: DocumentMethod.outliersLocalFactor,
      label: "Local Outlier Factor",
    },
    {
      value: DocumentMethod.outliersOneClassSvm,
      label: "One Class SVM",
    },
  ],
  [BtnGroups.group4]: [
    {
      value: DocumentMethod.fsSelectPercentile,
      label: "По перцентилю",
    },
    {
      value: DocumentMethod.fsSelectKBest,
      label: "По K лучшим",
    },
    {
      value: DocumentMethod.fsSelectFpr,
      label: "FPR",
    },
    {
      value: DocumentMethod.fsSelectFdr,
      label: "FDR",
    },
    {
      value: DocumentMethod.fsSelectFwe,
      label: "FWE",
    },
    {
      value: DocumentMethod.fsSelectRfe,
      label: "RFE",
    },
    {
      value: DocumentMethod.fsSelectFromModel,
      label: "Из линейной модели",
    },
    {
      value: DocumentMethod.fsSelectPca,
      label: "Метод главных компонент",
    },
  ],
};

export const MethodHeaders = values(ButtonsData).flat();

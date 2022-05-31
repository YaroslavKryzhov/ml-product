import * as React from "react";
import Typography from "@mui/material/Typography";
import { Box, Paper, Stack, styled } from "@mui/material";
import { theme } from "globalStyle/theme";
import { LoadingButton } from "@mui/lab";
import { DocumentMethod } from "ducks/reducers/types";
import {
  useApplyDocMethodMutation,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { useParams } from "react-router-dom";
import { UnavailableBlock } from "./common";

enum BtnGroups {
  group1 = "group1",
  group2 = "group2",
  group3 = "group3",
  group4 = "group4",
}

const ButtonsGroupsLabels = {
  [BtnGroups.group1]: "Обработка данных",
  [BtnGroups.group2]: "Трансформация признаков",
  [BtnGroups.group3]: "Удаление выбросов",
  [BtnGroups.group4]: "Отбор признаков",
};

const ButtonsData = {
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
      label: "IsolationForest",
    },
    {
      value: DocumentMethod.outliersEllipticEnvelope,
      label: "EllipticEnvelope",
    },
    {
      value: DocumentMethod.outliersLocalFactor,
      label: "LocalOutlierFactor",
    },
    {
      value: DocumentMethod.outliersOneClassSvm,
      label: "OneClassSVM",
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

export const DocumentMethods: React.FC = () => {
  const { docName } = useParams();

  const { data: infoData } = useInfoDocumentQuery(docName!);
  const [applyMethod, { isLoading }] = useApplyDocMethodMutation();

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Методы
      </Typography>

      {infoData?.column_types ? (
        <Stack
          sx={{
            columnGap: theme.spacing(2),
            rowGap: theme.spacing(3),
            flexWrap: "wrap",
            justifyContent: "center",
          }}
          direction="row"
        >
          {Object.values(BtnGroups).map((groupKey) => (
            <Paper
              sx={{
                backgroundColor: theme.palette.secondary.light,
                padding: theme.spacing(3),
                flexGrow: 1,
                maxWidth: "33%",
              }}
              key={groupKey}
              elevation={3}
            >
              <Typography
                variant="h6"
                sx={{ textAlign: "center", mb: theme.spacing(2) }}
              >
                {ButtonsGroupsLabels[groupKey]}
              </Typography>

              <Stack
                sx={{
                  gap: theme.spacing(1),
                  flexWrap: "wrap",
                }}
              >
                {ButtonsData[groupKey].map((act) => (
                  <LoadingButton
                    loading={isLoading}
                    variant="contained"
                    key={act.value}
                    sx={{
                      flexGrow: 1,
                    }}
                    onClick={() =>
                      applyMethod({
                        function_name: act.value,
                        filename: docName!,
                      })
                    }
                  >
                    {act.label}
                  </LoadingButton>
                ))}
              </Stack>
            </Paper>
          ))}
        </Stack>
      ) : (
        <UnavailableBlock label="Методы доступны только после разметки" />
      )}
    </Box>
  );
};

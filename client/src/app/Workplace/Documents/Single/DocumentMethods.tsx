import * as React from "react";
import MuiAccordion, { AccordionProps } from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Box, Stack, styled } from "@mui/material";
import { theme } from "globalStyle/theme";
import { LoadingButton } from "@mui/lab";
import { DocumentMethod } from "ducks/reducers/types";
import { useApplyDocMethodMutation } from "ducks/reducers/api/documents.api";

enum BtnGroups {
  group1 = "group1",
  group2 = "group2",
  group3 = "group3",
}

const ButtonsData = {
  [BtnGroups.group1]: [
    { value: DocumentMethod.removeDuplicates, label: "Удалить дубликаты" },
    { value: DocumentMethod.dropNa, label: "Удалить пропуски" },
    {
      value: DocumentMethod.missInsertMeanMode,
      label: DocumentMethod.missInsertMeanMode,
    },
    {
      value: DocumentMethod.missLinearImputer,
      label: DocumentMethod.missLinearImputer,
    },
  ],
  [BtnGroups.group2]: [
    { value: DocumentMethod.standartizeFeatures, label: "Стандартизация" },
    {
      value: DocumentMethod.ordinalEncoding,
      label: DocumentMethod.ordinalEncoding,
    },
    {
      value: DocumentMethod.oneHotEncoding,
      label: DocumentMethod.oneHotEncoding,
    },
  ],
  [BtnGroups.group3]: [
    {
      value: DocumentMethod.outliersIsolationForest,
      label: DocumentMethod.outliersIsolationForest,
    },
    {
      value: DocumentMethod.outliersEllipticEnvelope,
      label: DocumentMethod.outliersEllipticEnvelope,
    },
    {
      value: DocumentMethod.outliersLocalFactor,
      label: DocumentMethod.outliersLocalFactor,
    },
    {
      value: DocumentMethod.outliersOneClassSvm,
      label: "outliers_one_class_svm",
    },
  ],
};

const Accordion = styled((props: AccordionProps) => (
  <MuiAccordion elevation={3} {...props} />
))(() => ({
  backgroundColor: theme.palette.secondary.light,
  marginBottom: theme.spacing(2),
}));

export const DocumentMethods: React.FC<{ docName: string }> = ({ docName }) => {
  const [applyMethod, { isLoading }] = useApplyDocMethodMutation();

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Методы
      </Typography>

      {Object.keys(ButtonsData).map((groupKey) => (
        <Accordion key={groupKey} expanded>
          <AccordionSummary>
            <Typography variant="h6">{groupKey}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack direction="row" sx={{ gap: theme.spacing(1) }}>
              {ButtonsData[groupKey as BtnGroups].map((act) => (
                <LoadingButton
                  loading={isLoading}
                  variant="contained"
                  key={act.value}
                  onClick={() =>
                    applyMethod({ function_name: act.value, filename: docName })
                  }
                >
                  {act.label}
                </LoadingButton>
              ))}
            </Stack>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

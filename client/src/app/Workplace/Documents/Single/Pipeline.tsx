import React from "react";
import { styled } from "@mui/material/styles";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import SettingsIcon from "@mui/icons-material/Settings";
import StepConnector, {
  stepConnectorClasses,
} from "@mui/material/StepConnector";
import { StepIconProps } from "@mui/material/StepIcon";
import { theme } from "globalStyle/theme";
import { Box, Divider, Paper, Typography } from "@mui/material";
import { DocumentMethod, PipelineUnit } from "ducks/reducers/types";
import { useParams } from "react-router-dom";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";
import { UnavailableBlock } from "./common";

const ColorlibConnector = styled(StepConnector)(({ theme }) => ({
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    top: 30,
  },
  [`& .${stepConnectorClasses.line}`]: {
    height: 3,
    border: 0,
    backgroundColor: theme.palette.primary.main,
  },
}));

const ColorlibStepIconRoot = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  zIndex: 1,
  color: theme.palette.primary.contrastText,
  width: 61,
  height: 61,
  display: "flex",
  borderRadius: "50%",
  justifyContent: "center",
  alignItems: "center",
}));

const ColorlibStepIcon: React.FC<StepIconProps> = (props: StepIconProps) => (
  <ColorlibStepIconRoot>
    <SettingsIcon />
  </ColorlibStepIconRoot>
);

const Labels: { [key: string]: string } = {
  [DocumentMethod.standardize_features]: "Стандартизация",
};

export const Pipeline: React.FC = () => {
  const { docName } = useParams();
  const { data: docInfo } = useInfoDocumentQuery(docName!);

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Пайплайн
      </Typography>
      {docInfo?.pipeline?.length ? (
        <Stepper
          sx={{
            width: (docInfo?.pipeline?.length || 0) * 200,
            border: `${theme.additional.borderWidth}px solid ${theme.palette.primary.main}`,
            p: theme.spacing(1),
            borderRadius: `${theme.shape.borderRadiusRound}px`,
          }}
          alternativeLabel
          connector={<ColorlibConnector />}
        >
          {docInfo?.pipeline.map((unit, inx) => (
            <Step
              key={inx}
              sx={{
                p: 0,
                "& .MuiStepLabel-label": {
                  lineHeight: theme.typography.body1.fontSize,
                },
              }}
            >
              <StepLabel StepIconComponent={ColorlibStepIcon}>
                {Labels[unit.function_name]}
              </StepLabel>
            </Step>
          ))}
        </Stepper>
      ) : (
        <UnavailableBlock label="Пока что пусто, примените методы" />
      )}
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

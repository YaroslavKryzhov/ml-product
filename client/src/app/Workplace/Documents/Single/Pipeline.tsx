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
import { Box, Divider, Typography } from "@mui/material";

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
  standardize_features: "Стандартизация",
};

export const Pipeline: React.FC<{ steps: string[] }> = ({ steps }) => {
  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Пайплайн
      </Typography>
      <Stepper
        sx={{
          width: steps.length * 200,
          border: `${theme.additional.borderWidth}px solid ${theme.palette.primary.main}`,
          p: theme.spacing(1),
          borderRadius: "30px",
        }}
        alternativeLabel
        connector={<ColorlibConnector />}
      >
        {steps.map((label, inx) => (
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
              {Labels[label]}
            </StepLabel>
          </Step>
        ))}
      </Stepper>
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

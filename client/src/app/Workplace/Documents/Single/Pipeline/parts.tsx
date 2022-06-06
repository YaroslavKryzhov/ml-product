import React from "react";
import SettingsIcon from "@mui/icons-material/Settings";
import { theme } from "globalStyle/theme";
import {
  Box,
  Paper,
  PopperProps,
  StepConnector,
  stepConnectorClasses,
  StepIconProps,
  styled,
  Typography,
} from "@mui/material";
import { PipelineUnit } from "ducks/reducers/types";
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";
import { BuildLabel } from "./helpers";

export const ColorlibConnector = styled(StepConnector)(({ theme }) => ({
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    top: 30,
  },
  [`& .${stepConnectorClasses.line}`]: {
    height: 3,
    border: 0,
    backgroundColor: theme.palette.primary.main,
  },
}));

export const ColorlibStepIconRoot = styled("div")(({ theme }) => ({
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

export const ColorlibStepIcon: React.FC<StepIconProps> = () => (
  <ColorlibStepIconRoot>
    <SettingsIcon />
  </ColorlibStepIconRoot>
);

const ConnectedPipelineList: React.FC<{ pipeline: PipelineUnit[] }> = ({
  pipeline,
}) => (
  <>
    {pipeline.map((x, inx) => (
      <Box key={inx} sx={{ display: "flex" }}>
        <SettingsIcon sx={{ mr: theme.spacing(1) }} />
        {BuildLabel(x)}
        {inx !== pipeline.length - 1 && (
          <ArrowRightAltIcon sx={{ m: `0 ${theme.spacing(2)}` }} />
        )}
      </Box>
    ))}
  </>
);

export const PipelinePopper: React.FC<
  PopperProps & { pipeline: PipelineUnit[] }
> = ({ anchorEl, open, pipeline }) => {
  const anchorRect = (anchorEl as HTMLElement)?.getBoundingClientRect();

  return (
    <Paper
      sx={{
        padding: `${theme.spacing(1)} ${theme.spacing(2)}`,
        position: "fixed",
        top: anchorRect?.top - parseInt(theme.spacing(1)),
        left: anchorRect?.right + parseInt(theme.spacing(2)),
        display: open ? "flex" : "none",
        flexWrap: "wrap",
      }}
    >
      <ConnectedPipelineList pipeline={pipeline} />
    </Paper>
  );
};

export const PipelineDialog: React.FC<{
  pipeline: PipelineUnit[];
  targetDoc: string;
  currentDoc: string;
}> = ({ pipeline, targetDoc, currentDoc }) => (
  <Box sx={{ textAlign: "center" }}>
    <Typography variant="body1" sx={{ mb: theme.spacing(5) }}>
      Вы действительно хотите применить пайплайн из <b>{targetDoc}</b> к{" "}
      <b>{currentDoc}</b>?
    </Typography>
    <Paper
      sx={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        padding: theme.spacing(2),
        background: theme.palette.secondary.light,
      }}
    >
      <ConnectedPipelineList pipeline={pipeline} />
    </Paper>
  </Box>
);

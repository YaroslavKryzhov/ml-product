import React, { useCallback, useMemo, useRef, useState } from "react";
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
import {
  Box,
  Button,
  Divider,
  Menu,
  MenuItem,
  Skeleton,
  Tooltip,
  Typography,
} from "@mui/material";
import CopyAllIcon from "@mui/icons-material/CopyAll";
import { useParams } from "react-router-dom";
import {
  useAllDocumentsQuery,
  useCopyPipelineMutation,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { UnavailableBlock } from "./common";
import { useAppDispatch } from "ducks/hooks";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { compose, flatten, map, prop, T, values, zipObj } from "ramda";
import { ButtonsData } from "./DocumentMethods/constants";
import { DocumentMethod } from "ducks/reducers/types";

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

const ColorlibStepIcon: React.FC<StepIconProps> = () => (
  <ColorlibStepIconRoot>
    <SettingsIcon />
  </ColorlibStepIconRoot>
);

const PipelineGroups = {
  ...ButtonsData,
  more: [{ label: "Удаление колонки", value: DocumentMethod.dropСolumn }],
};

export const Pipeline: React.FC = () => {
  const { docName } = useParams();
  const { data: docInfo, isFetching: docInfoLoading } = useInfoDocumentQuery(
    docName!
  );
  const { data: allDocuments } = useAllDocumentsQuery();
  const [copyPipeline] = useCopyPipelineMutation();
  const dispatch = useAppDispatch();

  const filteredDocs = useMemo(
    () =>
      allDocuments?.filter(
        (doc) => doc.name !== docName && doc.pipeline?.length
      ),
    [allDocuments, docName]
  );
  const [fromDocumentMenuOpened, setDromDocumentMenuOpened] = useState(false);
  const anchorEl = useRef<HTMLButtonElement>(null);
  const applyPipelineConfirm = useCallback(
    (fromDocName: string) => () => {
      setDromDocumentMenuOpened(false);
      dispatch(
        setDialog({
          title: "Применить пайплайн",
          text: `Вы действительно хотите применить пайплайн из ${fromDocName} к ${docName}?`,
          onAccept: async () => {
            dispatch(setDialogLoading(true));
            await copyPipeline({ from: fromDocName, to: docName! });
            dispatch(setDialogLoading(false));
          },
          onDismiss: T,
        })
      );
    },
    [docName, copyPipeline, dispatch]
  );

  const mapPath = useCallback(
    (key: string) =>
      (compose as any)(
        map(prop(key)),
        flatten,
        values
      )(PipelineGroups) as string[],
    []
  );

  const labels = useMemo(
    () => zipObj(mapPath("value"), mapPath("label")),
    [mapPath]
  );

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Пайплайн
        {!!allDocuments?.length && (
          <>
            <Tooltip
              followCursor
              disableHoverListener={!!filteredDocs?.length}
              title="Не найдено документов с непустым пайплайном"
            >
              <Button
                disabled={!filteredDocs?.length}
                ref={anchorEl}
                sx={{ ml: theme.spacing(3) }}
                size="small"
                variant="outlined"
                endIcon={<CopyAllIcon />}
                onClick={() => setDromDocumentMenuOpened(true)}
              >
                Применить из
              </Button>
            </Tooltip>
            <Menu
              PaperProps={{ sx: { mt: theme.spacing(1) } }}
              anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
              transformOrigin={{ vertical: "top", horizontal: "center" }}
              onClose={() => setDromDocumentMenuOpened(false)}
              anchorEl={anchorEl.current}
              open={fromDocumentMenuOpened}
            >
              {filteredDocs?.map((doc) => (
                <MenuItem
                  key={doc.name}
                  onClick={applyPipelineConfirm(doc.name)}
                  sx={{ padding: `${theme.spacing(0.5)} ${theme.spacing(1)}` }}
                >
                  {doc.name}
                </MenuItem>
              ))}
            </Menu>
          </>
        )}
      </Typography>
      {docInfoLoading ? (
        <Skeleton variant="rectangular" width="100%" height={132} />
      ) : (
        <>
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
                    <Box sx={{ padding: `0 ${theme.spacing(1)}` }}>
                      {`${labels[unit.function_name]} ${
                        unit.param ? `(${unit.param})` : ""
                      }`}
                    </Box>
                  </StepLabel>
                </Step>
              ))}
            </Stepper>
          ) : (
            <UnavailableBlock label="Пока что пусто, примените методы" />
          )}
        </>
      )}

      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

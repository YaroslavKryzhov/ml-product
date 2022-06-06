import React, { useCallback, useMemo, useRef, useState } from "react";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
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
import { UnavailableBlock } from "../common";
import { useAppDispatch } from "ducks/hooks";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { T } from "ramda";
import {
  ColorlibConnector,
  ColorlibStepIcon,
  PipelineDialog,
  PipelinePopper,
} from "./parts";
import { BuildLabel } from "./helpers";
import { DocumentInfoShort } from "ducks/reducers/types";

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
    (fromDoc: DocumentInfoShort) => () => {
      setDromDocumentMenuOpened(false);
      dispatch(
        setDialog({
          title: "Применить пайплайн",
          Content: (
            <PipelineDialog
              currentDoc={docName!}
              targetDoc={fromDoc.name}
              pipeline={fromDoc.pipeline}
            />
          ),
          onAccept: async () => {
            dispatch(setDialogLoading(true));
            await copyPipeline({ from: fromDoc.name, to: docName! });
            dispatch(setDialogLoading(false));
          },
          onDismiss: T,
        })
      );
    },
    [docName, copyPipeline, dispatch]
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
                <Tooltip
                  PopperComponent={PipelinePopper as any}
                  PopperProps={{ pipeline: doc.pipeline } as any}
                  key={doc.name}
                  title="test"
                >
                  <MenuItem
                    onClick={applyPipelineConfirm(doc)}
                    sx={{
                      padding: `${theme.spacing(0.5)} ${theme.spacing(1)}`,
                    }}
                  >
                    {doc.name}
                  </MenuItem>
                </Tooltip>
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
                      {BuildLabel(unit)}
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

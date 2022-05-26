import { LoadingButton } from "@mui/lab";
import {
  Box,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  useColumnMarksDocumentQuery,
  useColumnsDocumentQuery,
  useSelectDocumentTargetMutation,
} from "ducks/reducers/api/documents.api";
import {
  changeSelectedTarget,
  changeSelectedTaskType,
} from "ducks/reducers/documents";
import { TaskType } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import React, { useCallback } from "react";
import { useParams } from "react-router-dom";
import { TASK_TYPE_LABEL } from "../List/constants";
import { UnavailableBlock } from "./common";

export const Markup: React.FC = () => {
  const { docName } = useParams();
  const { selectedTargetColumn, selectedTaskType } = useSESelector(
    (state) => state.documents
  );
  const [saveMarkup, { isLoading: isSaving }] =
    useSelectDocumentTargetMutation();
  const { data: columns } = useColumnsDocumentQuery(docName!);
  const { isError: columnMarksError } = useColumnMarksDocumentQuery(docName!);

  const dispatch = useAppDispatch();

  const onSaveClick = useCallback(() => {
    if (docName && selectedTargetColumn && selectedTaskType)
      saveMarkup({
        filename: docName,
        targetColumn: selectedTargetColumn,
        taskType: selectedTaskType,
      });
  }, [selectedTargetColumn, selectedTaskType, docName]);

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Разметка
      </Typography>
      {columnMarksError && (
        <UnavailableBlock label=" Внимание, вы сможете произвести разметку только один раз!!! Будьте Внимательны!!!" />
      )}
      <Box
        sx={{
          mt: theme.spacing(3),
          display: "flex",
          gap: theme.spacing(6),
        }}
      >
        <FormControl sx={{ width: "400px" }}>
          <InputLabel>Target</InputLabel>

          <Select
            value={selectedTargetColumn || ""}
            label="Target"
            onChange={(event) =>
              dispatch(changeSelectedTarget(event.target.value))
            }
          >
            {columns?.map((x) => (
              <MenuItem value={x}>{x}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: "400px" }}>
          <InputLabel>Task Type</InputLabel>
          <Select
            value={selectedTaskType || ""}
            label="Task Type"
            onChange={(event) =>
              dispatch(changeSelectedTaskType(event.target.value as TaskType))
            }
          >
            <MenuItem value={TaskType.classification}>
              {TASK_TYPE_LABEL.classification}
            </MenuItem>
            <MenuItem value={TaskType.regression}>
              {TASK_TYPE_LABEL.regression}
            </MenuItem>
          </Select>
        </FormControl>
        <LoadingButton
          disabled={!selectedTargetColumn || !selectedTaskType}
          onClick={onSaveClick}
          loading={isSaving}
          variant="contained"
        >
          Сохранить
        </LoadingButton>
      </Box>
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

import { LoadingButton } from "@mui/lab";
import {
  Box,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Skeleton,
  Stack,
  Typography,
} from "@mui/material";
import { UnavailableBlock } from "app/Workplace/common/UnavailableBlock";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  useColumnsDocumentQuery,
  useSelectDocumentTargetMutation,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { changeSelectedTarget } from "ducks/reducers/documents";
import { theme } from "globalStyle/theme";
import React from "react";
import { useParams } from "react-router-dom";

export const Markup: React.FC = () => {
  const { docId } = useParams();
  const { selectedTargetColumn, selectedTaskType } = useSESelector(
    (state) => state.documents
  );
  const [saveMarkup, { isLoading: isSaving }] =
    useSelectDocumentTargetMutation();
  const { data: columns, isFetching: columnsLoading } = useColumnsDocumentQuery(
    docId!
  );
  const { data: docInfo, isFetching: docInfoLoading } = useInfoDocumentQuery(
    docId!
  );

  const dispatch = useAppDispatch();

  const onSaveClick = () => {
    if (docId && selectedTargetColumn && selectedTaskType)
      saveMarkup({
        dataframe_id: docId,
        target_column: selectedTargetColumn,
      });
  };

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(3) }} variant="h5">
        Разметка
      </Typography>
      {docInfoLoading || columnsLoading ? (
        <Stack
          direction="row"
          gap={theme.spacing(6)}
          sx={{ mt: theme.spacing(3) }}
        >
          <Skeleton variant="rectangular" width={400} height={60} />
          <Skeleton variant="rectangular" width={400} height={60} />
        </Stack>
      ) : (
        <>
          {!docInfo?.column_types.target && (
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
                disabled={Boolean(docInfo?.column_types.target)}
                value={
                  docInfo?.column_types?.target || selectedTargetColumn || ""
                }
                label="Target"
                onChange={(event) =>
                  dispatch(changeSelectedTarget(event.target.value))
                }
              >
                {columns?.map((x) => (
                  <MenuItem key={x} value={x}>
                    {x}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            {/* <FormControl disabled sx={{ width: "400px" }}>
              <InputLabel>Task Type</InputLabel>
              <Select
                disabled={true || !!docInfo?.column_types}
                value={
                  docInfo?.column_types?.task_type || selectedTaskType || ""
                }
                label="Task Type"
                onChange={(event) =>
                  dispatch(
                    changeSelectedTaskType(event.target.value as TaskType)
                  )
                }
              >
                <MenuItem value={TaskType.classification}>
                  {TASK_TYPE_LABEL.classification}
                </MenuItem>
                <MenuItem value={TaskType.regression}>
                  {TASK_TYPE_LABEL.regression}
                </MenuItem>
              </Select>
            </FormControl> */}
            {!docInfo?.column_types.target && (
              <LoadingButton
                disabled={!selectedTargetColumn || !selectedTaskType}
                onClick={onSaveClick}
                loading={isSaving}
                variant="contained"
              >
                Сохранить
              </LoadingButton>
            )}
          </Box>
        </>
      )}
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

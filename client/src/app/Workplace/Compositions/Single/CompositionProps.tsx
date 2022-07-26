import {
  Box,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Tooltip,
  Typography,
} from "@mui/material";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { useAllDocumentsQuery } from "ducks/reducers/api/documents.api";
import {
  changeTaskType,
  changeCompositionType,
  changeParamsType,
  changeDocumentName,
  changeTestSize,
} from "ducks/reducers/compositions";
import {
  CompositionType,
  ParamsCompositionType,
  TaskType,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import React from "react";

export const CompositionProps: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  const { taskType, compositionType, paramsType, documentName, testSize } =
    useSESelector((state) => state.compositions);
  const dispatch = useAppDispatch();
  const { data: allDocuments, isFetching } = useAllDocumentsQuery();

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Основное
      </Typography>
      <Box
        sx={{
          mt: theme.spacing(3),
          display: "flex",
          gap: theme.spacing(1),
          flexWrap: "wrap",
        }}
      >
        <FormControl sx={{ width: "190px" }}>
          <InputLabel>Task Type</InputLabel>
          <Select
            disabled={!createMode}
            value={taskType}
            label="Task Type"
            onChange={(event) =>
              dispatch(changeTaskType(event.target.value as TaskType))
            }
          >
            {values(TaskType)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: "190px" }}>
          <InputLabel>Composition Type</InputLabel>
          <Select
            disabled={!createMode}
            value={compositionType}
            label="Composition Type"
            onChange={(event) =>
              dispatch(
                changeCompositionType(event.target.value as CompositionType)
              )
            }
          >
            {values(CompositionType)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: "190px" }}>
          <InputLabel>Params Type</InputLabel>
          <Select
            disabled={!createMode}
            value={paramsType}
            label="Params Type"
            onChange={(event) =>
              dispatch(
                changeParamsType(event.target.value as ParamsCompositionType)
              )
            }
          >
            {values(ParamsCompositionType)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: "190px" }}>
          <InputLabel>Document</InputLabel>
          <Select
            disabled={!createMode && isFetching}
            value={documentName}
            label="Document"
            onChange={(event) =>
              dispatch(changeDocumentName(event.target.value))
            }
          >
            {allDocuments?.map(({ name }) => (
              <MenuItem key={name} value={name}>
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Box sx={{ width: "190px", ml: theme.spacing(3) }}>
          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <Typography variant="body2">Test Size</Typography>
            <Typography variant="body2">{testSize}</Typography>
          </Box>

          <Slider
            value={testSize}
            min={0}
            step={0.01}
            max={1}
            onChange={(_, val) => dispatch(changeTestSize(val as number))}
          />
        </Box>
      </Box>

      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

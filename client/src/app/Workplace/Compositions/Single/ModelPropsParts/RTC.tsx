import {
  Box,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import {
  RandomForestClassifierParameters,
  DescicionSplitter,
  DesicionCriterion,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { useState } from "react";
import {
  MIN_SAMPLES_LEAF,
  MIN_SAMPLES_SPLIT,
  SELECTORS_WIDTH,
} from "../constants";

export const RandomForestClassifier: React.FC<{
  onParamsChange: (params: RandomForestClassifierParameters) => void;
  params: RandomForestClassifierParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => {
  const [isMaxDepthEnabled, setIsMaxDepthEnabled] = useState<boolean>(false);

  return (
    <Box sx={{ mt: theme.spacing(5) }}>
      <Box
        sx={{
          display: "flex",
          gap: `${theme.spacing(2)} ${theme.spacing(1)}`,
          flexWrap: "wrap",
        }}
      >
        <FormControl sx={{ width: SELECTORS_WIDTH }}>
          <InputLabel>Criterion</InputLabel>
          <Select
            disabled={disabled}
            value={params.criterion}
            label="Criterion"
            onChange={(event) =>
              onParamsChange({
                ...params,
                criterion: event.target.value as DesicionCriterion,
              })
            }
          >
            {values(DesicionCriterion)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: SELECTORS_WIDTH }}>
          <InputLabel>Splitter</InputLabel>
          <Select
            disabled={disabled}
            value={params.splitter}
            label="Splitter"
            onChange={(event) =>
              onParamsChange({
                ...params,
                splitter: event.target.value as DescicionSplitter,
              })
            }
          >
            {values(DescicionSplitter)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Min Samples Split"
          value={params.min_samples_split}
          onChange={(event) =>
            Number(event.target.value) >= MIN_SAMPLES_SPLIT &&
            onParamsChange({
              ...params,
              min_samples_split: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Min Samples Leaf"
          value={params.min_samples_leaf}
          onChange={(event) =>
            Number(event.target.value) >= MIN_SAMPLES_LEAF &&
            onParamsChange({
              ...params,
              min_samples_leaf: Number(event.target.value),
            })
          }
          type="number"
        />
      </Box>
      <Box
        sx={{
          display: "grid",
          mt: theme.spacing(5),
          mb: theme.spacing(2),
          gap: theme.spacing(2),
          gridTemplateColumns: "repeat(2, max-content)",
        }}
      >
        <Box
          sx={{
            display: "grid",
            gap: theme.spacing(2),
          }}
        >
          <Box sx={{ display: "grid" }}>
            <FormControlLabel
              control={
                <Checkbox
                  value={isMaxDepthEnabled}
                  onChange={(_, checked) => {
                    setIsMaxDepthEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        max_depth: null,
                      });
                  }}
                />
              }
              label="Max Depth Enabled"
            />
          </Box>
        </Box>
      </Box>
      <Box
        sx={{
          display: "flex",
          gap: `${theme.spacing(2)} ${theme.spacing(1)}`,
          flexWrap: "wrap",
        }}
      >
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled || !isMaxDepthEnabled}
          label="Max depth"
          value={params.max_depth || ""}
          onChange={(event) =>
            Number(event.target.value) > 0 &&
            onParamsChange({
              ...params,
              max_depth: Number(event.target.value),
            })
          }
          type="number"
        />
      </Box>
      <Box
        sx={{
          mt: theme.spacing(5),
          gap: theme.spacing(2),
        }}
      >
        <FormControlLabel
          control={
            <Checkbox
              value={params.bootstrap}
              onChange={(_, checked) => {
                onParamsChange({
                  ...params,
                  bootstrap: checked,
                });
              }}
            />
          }
          label="bootstrap"
        />
      </Box>
    </Box>
  );
};

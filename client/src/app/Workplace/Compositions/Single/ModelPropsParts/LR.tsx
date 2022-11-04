import {
  Box,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  TextField,
  Typography,
} from "@mui/material";
import {
  LogisticRegressionParameters,
  LogisticRegressionPenalty,
  LogisticRegressionSolver,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { useState } from "react";
import { SELECTORS_WIDTH } from "../constants";

export const LogisticRegression: React.FC<{
  onParamsChange: (params: LogisticRegressionParameters) => void;
  params: LogisticRegressionParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => {
  const [isL1RatioEnabled, setIsL1RatioEnabled] = useState(false);

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
          <InputLabel>penalty</InputLabel>
          <Select
            disabled={disabled}
            value={params.penalty}
            label="penalty"
            onChange={(event) =>
              onParamsChange({
                ...params,
                penalty: event.target.value as LogisticRegressionPenalty,
              })
            }
          >
            {values(LogisticRegressionPenalty)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: SELECTORS_WIDTH }}>
          <InputLabel>solver</InputLabel>
          <Select
            disabled={disabled}
            value={params.solver}
            label="solver"
            onChange={(event) =>
              onParamsChange({
                ...params,
                solver: event.target.value as LogisticRegressionSolver,
              })
            }
          >
            {values(LogisticRegressionSolver)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="C"
          value={params.C}
          onChange={(event) =>
            Number(event.target.value) > 0 &&
            onParamsChange({
              ...params,
              C: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="max_iter"
          value={params.max_iter}
          onChange={(event) =>
            Number(event.target.value) > 0 &&
            onParamsChange({
              ...params,
              max_iter: Number(event.target.value),
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
              value={params.fit_intercept}
              onChange={(_, checked) => {
                onParamsChange({
                  ...params,
                  fit_intercept: checked,
                });
              }}
            />
          }
          label="fit_intercept"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={params.dual}
              onChange={(_, checked) => {
                onParamsChange({
                  ...params,
                  dual: checked,
                });
              }}
            />
          }
          label="dual"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={isL1RatioEnabled}
              onChange={(_, checked) => {
                setIsL1RatioEnabled(checked);
                onParamsChange({
                  ...params,
                  l1_ratio: checked ? 0.1 : null,
                });
              }}
            />
          }
          label="l1 ratio enabled"
        />
      </Box>
      {isL1RatioEnabled && (
        <Box
          sx={{
            mt: theme.spacing(5),
          }}
        >
          <Box sx={{ width: SELECTORS_WIDTH }}>
            <Box sx={{ display: "flex", justifyContent: "space-between" }}>
              <Typography variant="body2">l1_ratio</Typography>
              <Typography variant="body2">{params.l1_ratio}</Typography>
            </Box>
            <Slider
              disabled={disabled}
              value={params.l1_ratio!}
              min={0}
              step={0.01}
              max={1}
              onChange={(_, val) =>
                onParamsChange({
                  ...params,
                  l1_ratio: Number(val),
                })
              }
            />
          </Box>
        </Box>
      )}
    </Box>
  );
};

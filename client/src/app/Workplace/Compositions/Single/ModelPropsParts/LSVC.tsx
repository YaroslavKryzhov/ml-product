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
  LinearSVCParameters,
  LinearSVCMultiClass,
  LinearSVCLoss,
  LinearSVCPenalty,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const LinearSVCClassifier: React.FC<{
  onParamsChange: (params: LinearSVCParameters) => void;
  params: LinearSVCParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => (
  <Box sx={{ mt: theme.spacing(5) }}>
    <Box
      sx={{
        display: "flex",
        gap: `${theme.spacing(2)} ${theme.spacing(1)}`,
        flexWrap: "wrap",
      }}
    >
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>loss</InputLabel>
        <Select
          disabled={disabled}
          value={params.loss}
          label="loss"
          onChange={(event) =>
            onParamsChange({
              ...params,
              loss: event.target.value as LinearSVCLoss,
            })
          }
        >
          {values(LinearSVCLoss)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>penalty</InputLabel>
        <Select
          disabled={disabled}
          value={params.penalty}
          label="penalty"
          onChange={(event) =>
            onParamsChange({
              ...params,
              penalty: event.target.value as LinearSVCPenalty,
            })
          }
        >
          {values(LinearSVCPenalty)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>multi_class</InputLabel>
        <Select
          disabled={disabled}
          value={params.multi_class}
          label="multi_class"
          onChange={(event) =>
            onParamsChange({
              ...params,
              multi_class: event.target.value as LinearSVCMultiClass,
            })
          }
        >
          {values(LinearSVCMultiClass)?.map((x) => (
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
    </Box>
  </Box>
);

import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import {
  KNeighborsClassifierParameters,
  KNeighborsWeights,
  KNeighborsAlgorithm,
  KNeighborsMetric,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const KNeighborsClassifier: React.FC<{
  onParamsChange: (params: KNeighborsClassifierParameters) => void;
  params: KNeighborsClassifierParameters;
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
        <InputLabel>weights</InputLabel>
        <Select
          disabled={disabled}
          value={params.weights}
          label="weights"
          onChange={(event) =>
            onParamsChange({
              ...params,
              weights: event.target.value as KNeighborsWeights,
            })
          }
        >
          {values(KNeighborsWeights)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>algorithm</InputLabel>
        <Select
          disabled={disabled}
          value={params.algorithm}
          label="algorithm"
          onChange={(event) =>
            onParamsChange({
              ...params,
              algorithm: event.target.value as KNeighborsAlgorithm,
            })
          }
        >
          {values(KNeighborsAlgorithm)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>metric</InputLabel>
        <Select
          disabled={disabled}
          value={params.metric}
          label="metric"
          onChange={(event) =>
            onParamsChange({
              ...params,
              metric: event.target.value as KNeighborsMetric,
            })
          }
        >
          {values(KNeighborsMetric)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="n_neighbors"
        value={params.n_neighbors}
        onChange={(event) =>
          Number(event.target.value) >= 1 &&
          onParamsChange({
            ...params,
            n_neighbors: Number(event.target.value),
          })
        }
        type="number"
      />
    </Box>
  </Box>
);

import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import {
  AdaBoostAlgorithm,
  AdaBoostClassifierParameters,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const AdaBoostClassifier: React.FC<{
  onParamsChange: (params: AdaBoostClassifierParameters) => void;
  params: AdaBoostClassifierParameters;
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
        <InputLabel>algorithm</InputLabel>
        <Select
          disabled={disabled}
          value={params.algorithm}
          label="algorithm"
          onChange={(event) =>
            onParamsChange({
              ...params,
              algorithm: event.target.value as AdaBoostAlgorithm,
            })
          }
        >
          {values(AdaBoostAlgorithm)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="n_estimators"
        value={params.n_estimators}
        onChange={(event) =>
          Number(event.target.value) >= 2 &&
          onParamsChange({
            ...params,
            n_estimators: Number(event.target.value),
          })
        }
        type="number"
      />
      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="learning_rate"
        value={params.learning_rate}
        onChange={(event) =>
          Number(event.target.value) > 0 &&
          onParamsChange({
            ...params,
            learning_rate: Number(event.target.value),
          })
        }
        type="number"
      />
    </Box>
  </Box>
);

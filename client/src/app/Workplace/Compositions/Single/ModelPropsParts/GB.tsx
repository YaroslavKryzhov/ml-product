import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  TextField,
  Typography,
} from "@mui/material";
import {
  GradientBoostingLoss,
  GradientBoostingCriterion,
  GradientBoostingClassifierParameters,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { MIN_SAMPLES_SPLIT, SELECTORS_WIDTH } from "../constants";

export const GradientBoostingClassifier: React.FC<{
  onParamsChange: (params: GradientBoostingClassifierParameters) => void;
  params: GradientBoostingClassifierParameters;
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
              loss: event.target.value as GradientBoostingLoss,
            })
          }
        >
          {values(GradientBoostingLoss)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>criterion</InputLabel>
        <Select
          disabled={disabled}
          value={params.criterion}
          label="criterion"
          onChange={(event) =>
            onParamsChange({
              ...params,
              criterion: event.target.value as GradientBoostingCriterion,
            })
          }
        >
          {values(GradientBoostingCriterion)?.map((x) => (
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
        label="max_depth"
        value={params.max_depth}
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
      }}
    >
      <Box sx={{ width: SELECTORS_WIDTH }}>
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <Typography variant="body2">subsample</Typography>
          <Typography variant="body2">{params.subsample}</Typography>
        </Box>
        <Slider
          disabled={disabled}
          value={params.subsample}
          min={0}
          step={0.01}
          max={1}
          onChange={(_, val) =>
            onParamsChange({
              ...params,
              subsample: Number(val),
            })
          }
        />
      </Box>
    </Box>
  </Box>
);

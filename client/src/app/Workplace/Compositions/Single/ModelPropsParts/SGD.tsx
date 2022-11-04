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
  SGDClassifierPenalty,
  SGDClassifierLearningRate,
  SGDClassifierLoss,
  SGDClassifierParameters,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const SGDClassifier: React.FC<{
  onParamsChange: (params: SGDClassifierParameters) => void;
  params: SGDClassifierParameters;
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
              loss: event.target.value as SGDClassifierLoss,
            })
          }
        >
          {values(SGDClassifierLoss)?.map((x) => (
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
              penalty: event.target.value as SGDClassifierPenalty,
            })
          }
        >
          {values(SGDClassifierPenalty)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ width: SELECTORS_WIDTH }}>
        <InputLabel>learning_rate</InputLabel>
        <Select
          disabled={disabled}
          value={params.learning_rate}
          label="learning_rate"
          onChange={(event) =>
            onParamsChange({
              ...params,
              learning_rate: event.target.value as SGDClassifierLearningRate,
            })
          }
        >
          {values(SGDClassifierLearningRate)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="alpha"
        value={params.alpha}
        onChange={(event) =>
          Number(event.target.value) >= 0 &&
          onParamsChange({
            ...params,
            alpha: Number(event.target.value),
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
      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="epsilon"
        value={params.epsilon}
        onChange={(event) =>
          Number(event.target.value) >= 0 &&
          onParamsChange({
            ...params,
            epsilon: Number(event.target.value),
          })
        }
        type="number"
      />
    </Box>

    <Box sx={{ width: SELECTORS_WIDTH, mt: theme.spacing(5) }}>
      <Box sx={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="body2">l1_ratio</Typography>
        <Typography variant="body2">{params.l1_ratio}</Typography>
      </Box>
      <Slider
        disabled={disabled}
        value={params.l1_ratio}
        min={0}
        step={0.01}
        max={1}
        onChange={(_, val) =>
          onParamsChange({
            ...params,
            l1_ratio: val as number,
          })
        }
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
            value={params.shuffle}
            onChange={(_, checked) => {
              onParamsChange({
                ...params,
                shuffle: checked,
              });
            }}
          />
        }
        label="shuffle"
      />
    </Box>
  </Box>
);

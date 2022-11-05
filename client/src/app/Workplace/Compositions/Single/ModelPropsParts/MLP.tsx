import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import {
  MLPClassifierParameters,
  MLPClassifierActivation,
  MLPClassifierSolver,
  MLPClassifierLearningRate,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const MLPClassifier: React.FC<{
  onParamsChange: (params: MLPClassifierParameters) => void;
  params: MLPClassifierParameters;
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
        <InputLabel>activation</InputLabel>
        <Select
          disabled={disabled}
          value={params.activation}
          label="activation"
          onChange={(event) =>
            onParamsChange({
              ...params,
              activation: event.target.value as MLPClassifierActivation,
            })
          }
        >
          {values(MLPClassifierActivation)?.map((x) => (
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
              solver: event.target.value as MLPClassifierSolver,
            })
          }
        >
          {values(MLPClassifierSolver)?.map((x) => (
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
              learning_rate: event.target.value as MLPClassifierLearningRate,
            })
          }
        >
          {values(MLPClassifierLearningRate)?.map((x) => (
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
    </Box>

    <Box
      sx={{
        mt: theme.spacing(5),
        display: "flex",
        gap: theme.spacing(1),
        alignItems: "center",
      }}
    >
      {params.hidden_layer_sizes.map((val, index) => (
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label={`hidden_layer_sizes[${index}]`}
          value={val}
          onChange={(event) =>
            Number(event.target.value) > 0 &&
            onParamsChange({
              ...params,
              hidden_layer_sizes: params.hidden_layer_sizes.map((x, i) =>
                i === index ? Number(event.target.value) : x
              ),
            })
          }
          type="number"
        />
      ))}
      <Box
        sx={{
          display: "flex",
          gap: theme.spacing(1),
          alignItems: "center",
        }}
      >
        <Button
          variant="contained"
          onClick={() =>
            onParamsChange({
              ...params,
              hidden_layer_sizes: params.hidden_layer_sizes.concat(0),
            })
          }
        >
          Add layer
        </Button>
        <Button
          variant="contained"
          onClick={() =>
            onParamsChange({
              ...params,
              hidden_layer_sizes: params.hidden_layer_sizes.slice(
                0,
                params.hidden_layer_sizes.length - 1
              ),
            })
          }
        >
          Delete layer
        </Button>
      </Box>
    </Box>
  </Box>
);

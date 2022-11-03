import { Box, Checkbox, FormControlLabel, TextField } from "@mui/material";
import { BaggingClassifierParameters } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { SELECTORS_WIDTH } from "../constants";

export const BaggingClassifier: React.FC<{
  onParamsChange: (params: BaggingClassifierParameters) => void;
  params: BaggingClassifierParameters;
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
        label="max_samples"
        value={params.max_samples}
        onChange={(event) =>
          Number(event.target.value) >= 1 &&
          onParamsChange({
            ...params,
            max_samples: Number(event.target.value),
          })
        }
        type="number"
      />
      <TextField
        sx={{ width: SELECTORS_WIDTH }}
        disabled={disabled}
        label="max_features"
        value={params.max_features}
        onChange={(event) =>
          Number(event.target.value) >= 1 &&
          onParamsChange({
            ...params,
            max_features: Number(event.target.value),
          })
        }
        type="number"
      />
    </Box>
    <Box
      sx={{
        display: "flex",
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
      <FormControlLabel
        control={
          <Checkbox
            value={params.bootstrap_features}
            onChange={(_, checked) => {
              onParamsChange({
                ...params,
                bootstrap_features: checked,
              });
            }}
          />
        }
        label="bootstrap_features"
      />
    </Box>
  </Box>
);

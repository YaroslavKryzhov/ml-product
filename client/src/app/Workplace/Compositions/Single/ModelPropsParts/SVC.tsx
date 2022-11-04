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
import { SVCKernel, SVCGamma, SVCParameters } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { useState } from "react";
import { SELECTORS_WIDTH } from "../constants";

const GAMMA_NUMBER = "GAMMA_NUMBER";

export const SVCClassifier: React.FC<{
  onParamsChange: (params: SVCParameters) => void;
  params: SVCParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => {
  const [isGammaNumber, setIsGammaNumber] = useState(false);
  const [maxIterAuto, setMaxIterAuto] = useState(true);

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
          <InputLabel>kernel</InputLabel>
          <Select
            disabled={disabled}
            value={params.kernel}
            label="kernel"
            onChange={(event) =>
              onParamsChange({
                ...params,
                kernel: event.target.value as SVCKernel,
              })
            }
          >
            {values(SVCKernel)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: SELECTORS_WIDTH }}>
          <InputLabel>gamma</InputLabel>
          <Select
            disabled={disabled}
            value={isGammaNumber ? GAMMA_NUMBER : params.gamma}
            label="gamma"
            onChange={(event) => {
              setIsGammaNumber(event.target.value === GAMMA_NUMBER);
              onParamsChange({
                ...params,
                gamma:
                  event.target.value === GAMMA_NUMBER
                    ? (event.target.value as SVCGamma)
                    : (0 as number),
              });
            }}
          >
            <MenuItem value={GAMMA_NUMBER}>Число</MenuItem>
            {values(SVCGamma)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {isGammaNumber && (
          <TextField
            sx={{ width: SELECTORS_WIDTH }}
            disabled={disabled}
            label="gamma"
            value={params.gamma}
            onChange={(event) =>
              onParamsChange({
                ...params,
                gamma: Number(event.target.value),
              })
            }
            type="number"
          />
        )}

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
          label="coef0"
          value={params.coef0}
          onChange={(event) =>
            Number(event.target.value) > 0 &&
            onParamsChange({
              ...params,
              coef0: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="degree"
          value={params.degree}
          onChange={(event) =>
            Number(event.target.value) >= 0 &&
            onParamsChange({
              ...params,
              degree: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled || maxIterAuto}
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
              value={params.shrinking}
              onChange={(_, checked) => {
                onParamsChange({
                  ...params,
                  shrinking: checked,
                });
              }}
            />
          }
          label="shrinking"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={maxIterAuto}
              onChange={(_, checked) => {
                setMaxIterAuto(checked);
                onParamsChange({
                  ...params,
                  max_iter: checked ? -1 : 1,
                });
              }}
            />
          }
          label="max_iter auto"
        />
      </Box>
    </Box>
  );
};

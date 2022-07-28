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
  DecisionTreeClassifierParameters,
  DescicionSplitter,
  DesicionCriterion,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { useState } from "react";
import { SELECTORS_WIDTH } from "../constants";

export const DecisionTreeClassifier: React.FC<{
  onParamsChange: (params: DecisionTreeClassifierParameters) => void;
  params: DecisionTreeClassifierParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => {
  const [isMaxDepthEnabled, setIsMaxDepthEnabled] = useState<boolean>(false);
  const [isMaxFeaturesEnabled, setIsMaxFeaturesEnabled] =
    useState<boolean>(false);
  const [isRandomStateEnabled, setIsRandomStateEnabled] =
    useState<boolean>(false);
  const [isMaxLeafNodesEnabled, setIsMaxLeafNodesEnabled] =
    useState<boolean>(false);
  const [isClassWeightEnabled, setIsClassWeightEnabled] =
    useState<boolean>(false);

  return (
    <Box sx={{ mt: theme.spacing(4) }}>
      <Box
        sx={{
          mb: theme.spacing(3),
        }}
      >
        <FormControlLabel
          control={
            <Checkbox
              value={isMaxDepthEnabled}
              onChange={(_, checked) => setIsMaxDepthEnabled(checked)}
            />
          }
          label="Max Depth Enabled"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={isMaxFeaturesEnabled}
              onChange={(_, checked) => setIsMaxFeaturesEnabled(checked)}
            />
          }
          label="Max Features Enabled"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={isRandomStateEnabled}
              onChange={(_, checked) => setIsRandomStateEnabled(checked)}
            />
          }
          label="Random State Enabled"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={isMaxLeafNodesEnabled}
              onChange={(_, checked) => setIsMaxLeafNodesEnabled(checked)}
            />
          }
          label="Max Leaf Nodes Enabled"
        />
        <FormControlLabel
          control={
            <Checkbox
              value={isClassWeightEnabled}
              onChange={(_, checked) => setIsClassWeightEnabled(checked)}
            />
          }
          label="Class Weight Enabled"
        />
      </Box>
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
          label="Max depth"
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

        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Min Samples Split"
          value={params.min_samples_split}
          onChange={(event) =>
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
            onParamsChange({
              ...params,
              min_samples_leaf: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Random State"
          value={params.random_state}
          onChange={(event) =>
            onParamsChange({
              ...params,
              random_state: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Max Leaf Nodes"
          value={params.max_leaf_nodes}
          onChange={(event) =>
            onParamsChange({
              ...params,
              max_leaf_nodes: Number(event.target.value),
            })
          }
          type="number"
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="Min Impurity Decrease"
          value={params.min_impurity_decrease}
          onChange={(event) =>
            onParamsChange({
              ...params,
              min_impurity_decrease: Number(event.target.value),
            })
          }
        />
        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="CCP Alpha"
          value={params.ccp_alpha}
          onChange={(event) =>
            onParamsChange({
              ...params,
              ccp_alpha: Number(event.target.value),
            })
          }
        />
      </Box>
    </Box>
  );
};

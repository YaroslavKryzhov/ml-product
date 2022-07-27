import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import {
  DecisionTreeClassifierParameters,
  DescicionSplitter,
  DesicionCriterion,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { values } from "lodash";
import { SELECTORS_WIDTH } from "../constants";

export const DecisionTreeClassifier: React.FC<{
  onParamsChange: (params: DecisionTreeClassifierParameters) => void;
  params: DecisionTreeClassifierParameters;
  disabled?: boolean;
}> = ({ onParamsChange, params, disabled }) => (
  <>
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
  </>
);

import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { changeModel } from "ducks/reducers/compositions";
import {
  DecisionTreeClassifierParameters,
  ModelTypes,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { cond, values } from "lodash";
import { always, equals } from "ramda";
import { useCallback } from "react";
import { DecisionTreeClassifier } from "./ModelPropsParts/DTC";

export const ModelProps: React.FC<{ id: string; createMode?: boolean }> = ({
  id,
  createMode,
}) => {
  const dispatch = useAppDispatch();
  const model = useSESelector((state) => state.compositions.models[id]);
  const onParamsChange = useCallback(() => {}, []);

  return (
    <Box sx={{ mb: theme.spacing(2) }}>
      <FormControl sx={{ width: "388px" }}>
        <InputLabel>Model Type</InputLabel>
        <Select
          disabled={!createMode}
          value={model.type}
          label="Model type"
          onChange={(event) =>
            dispatch(
              changeModel({
                id,
                model: {
                  type: event.target.value as ModelTypes,
                  params: {},
                },
              })
            )
          }
        >
          {values(ModelTypes)?.map((x) => (
            <MenuItem key={x} value={x}>
              {x}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {model.type && (
        <Box
          sx={{
            mt: theme.spacing(2),
            display: "flex",
            gap: theme.spacing(1),
            flexWrap: "wrap",
          }}
        >
          {cond<ModelTypes, JSX.Element | null>([
            [
              equals<ModelTypes>(ModelTypes.DecisionTreeClassifier),
              always(
                <DecisionTreeClassifier
                  onParamsChange={onParamsChange}
                  params={model.params as DecisionTreeClassifierParameters}
                  disabled={!createMode}
                />
              ),
            ],
          ])(model.type)}
        </Box>
      )}
    </Box>
  );
};

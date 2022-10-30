import {
  Box,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { changeModel, deleteModel } from "ducks/reducers/compositions";
import {
  DecisionTreeClassifierParameters,
  RandomForestClassifierParameters,
  ModelParams,
  ModelTypes,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { cond, values } from "lodash";
import { always, equals } from "ramda";
import ClearIcon from "@mui/icons-material/Clear";
import { DefaultParamsModels } from "./constants";
import { DecisionTreeClassifier } from "./ModelPropsParts/DTC";
import { RandomForestClassifier } from "./ModelPropsParts/RTC";

export const ModelProps: React.FC<{ id: string; createMode?: boolean }> = ({
  id,
  createMode,
}) => {
  const dispatch = useAppDispatch();
  const model = useSESelector((state) => state.compositions.models[id]);
  const onParamsChange =
    (type: ModelTypes, id: string) => (params: ModelParams) =>
      dispatch(
        changeModel({
          id,
          model: {
            type,
            params,
          },
        })
      );

  const onModelDelete = () => dispatch(deleteModel(id));
  return (
    <Box
      sx={{
        mb: theme.spacing(5),
        pl: theme.spacing(2),
        borderLeft: `2px solid ${theme.palette.info.main}`,
      }}
    >
      <Box
        sx={{ display: "flex", alignItems: "center", gap: theme.spacing(1) }}
      >
        <FormControl sx={{ width: "388px" }}>
          <InputLabel>Model Type</InputLabel>
          <Select
            disabled={!createMode}
            value={model.type || ""}
            label="Model type"
            onChange={(event) =>
              dispatch(
                changeModel({
                  id,
                  model: {
                    type: event.target.value as ModelTypes,
                    params:
                      DefaultParamsModels[event.target.value as ModelTypes]!,
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
        <IconButton disabled={!createMode}>
          <ClearIcon onClick={onModelDelete} />
        </IconButton>
      </Box>

      {model.type &&
        cond<ModelTypes, JSX.Element | null>([
          [
            equals<ModelTypes>(ModelTypes.DecisionTreeClassifier),
            always(
              <DecisionTreeClassifier
                onParamsChange={onParamsChange(model.type, id)}
                params={model.params as DecisionTreeClassifierParameters}
                disabled={!createMode}
              />
            ),
          ],
          [
            equals<ModelTypes>(ModelTypes.RandomForestClassifier),
            always(
              <RandomForestClassifier
                onParamsChange={onParamsChange(model.type, id)}
                params={model.params as RandomForestClassifierParameters}
                disabled={!createMode}
              />
            ),
          ],
        ])(model.type)}
    </Box>
  );
};

import {
  Box,
  Checkbox,
  FormControl,
  FormControlLabel,
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
  AdaBoostClassifierParameters,
  GradientBoostingClassifierParameters,
  BaggingClassifierParameters,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { cond, values } from "lodash";
import { always, equals } from "ramda";
import ClearIcon from "@mui/icons-material/Clear";
import { DefaultParamsModels } from "./constants";
import { DecisionTreeClassifier } from "./ModelPropsParts/DTC";
import { RandomForestClassifier } from "./ModelPropsParts/RTC";
import { AdaBoostClassifier } from "./ModelPropsParts/ADB";
import { GradientBoostingClassifier } from "./ModelPropsParts/GB";
import { BaggingClassifier } from "./ModelPropsParts/Bagging";

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

        <FormControlLabel
          sx={{ ml: theme.spacing(0) }}
          control={
            <Checkbox
              value={true}
              onChange={(_, checked) =>
                dispatch(
                  changeModel({
                    id,
                    model: {
                      ...model,
                      isDefaultParams: checked,
                    },
                  })
                )
              }
            />
          }
          disabled={!createMode}
          label="Default params"
        />
        <IconButton disabled={!createMode}>
          <ClearIcon onClick={onModelDelete} />
        </IconButton>
      </Box>

      {model.type &&
        !model.isDefaultParams &&
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
          [
            equals<ModelTypes>(ModelTypes.AdaBoostClassifier),
            always(
              <AdaBoostClassifier
                onParamsChange={onParamsChange(model.type, id)}
                params={model.params as AdaBoostClassifierParameters}
                disabled={!createMode}
              />
            ),
          ],
          [
            equals<ModelTypes>(ModelTypes.GradientBoostingClassifier),
            always(
              <GradientBoostingClassifier
                onParamsChange={onParamsChange(model.type, id)}
                params={model.params as GradientBoostingClassifierParameters}
                disabled={!createMode}
              />
            ),
          ],
          [
            equals<ModelTypes>(ModelTypes.BaggingClassifier),
            always(
              <BaggingClassifier
                onParamsChange={onParamsChange(model.type, id)}
                params={model.params as BaggingClassifierParameters}
                disabled={!createMode}
              />
            ),
          ],
        ])(model.type)}
    </Box>
  );
};

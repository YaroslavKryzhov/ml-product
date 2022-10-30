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
  // const [isMaxFeaturesEnabled, setIsMaxFeaturesEnabled] =
  //   useState<boolean>(false);
  // const [isRandomStateEnabled, setIsRandomStateEnabled] =
  //   useState<boolean>(false);
  // const [isMaxLeafNodesEnabled, setIsMaxLeafNodesEnabled] =
  //   useState<boolean>(false);
  // const [isClassWeightEnabled, setIsClassWeightEnabled] =
  //   useState<boolean>(false);

  // const [isMaxFeaturesFloat, setIsMaxFeaturesFloat] = useState<boolean>(false);
  // const [isClassWeightCustom, setIsClassWeightCustom] =
  //   useState<boolean>(false);

  // const [customClassWeights, setCustomClassWeights] = useState<
  //   Record<string, { label: string; value: string }>
  // >(
  //   isObject(params.class_weight)
  //     ? zipObject(
  //         values(params.class_weight).map(() => nanoid()),
  //         entries(params.class_weight).map(([label, value]) => ({
  //           label,
  //           value,
  //         }))
  //       )
  //     : {}
  // );

  // const updateWeights = useCallback(() => {
  //   onParamsChange({
  //     ...params,
  //     class_weight: Object.fromEntries(
  //       values(customClassWeights).map((x) => [x.label, x.value])
  //     ),
  //   });
  // }, [customClassWeights, onParamsChange, params]);

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
        {/* <TextField
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
        /> */}
        {/* <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled}
          label="CCP Alpha"
          value={params.ccp_alpha}
          onChange={(event) =>
            Number(event.target.value) >= 0 &&
            onParamsChange({
              ...params,
              ccp_alpha: Number(event.target.value),
            })
          }
        /> */}
      </Box>
      <Box
        sx={{
          display: "grid",
          mt: theme.spacing(5),
          mb: theme.spacing(2),
          gap: theme.spacing(2),
          gridTemplateColumns: "repeat(2, max-content)",
        }}
      >
        <Box
          sx={{
            display: "grid",
            gap: theme.spacing(2),
          }}
        >
          <Box sx={{ display: "grid" }}>
            <FormControlLabel
              disabled={disabled}
              control={
                <Checkbox
                  value={isMaxDepthEnabled}
                  onChange={(_, checked) => {
                    setIsMaxDepthEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        max_depth: null,
                      });
                  }}
                />
              }
              label="Max Depth Enabled"
            />
            {/* <FormControlLabel
              control={
                <Checkbox
                  value={isMaxFeaturesEnabled}
                  onChange={(_, checked) => {
                    setIsMaxFeaturesEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        max_features: null,
                      });
                  }}
                />
              }
              label="Max Features Enabled"
            /> */}
            {/* <FormControlLabel
              control={
                <Checkbox
                  value={isRandomStateEnabled}
                  onChange={(_, checked) => {
                    setIsRandomStateEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        random_state: null,
                      });
                  }}
                />
              }
              label="Random State Enabled"
            /> */}
            {/* <FormControlLabel
              control={
                <Checkbox
                  value={isMaxLeafNodesEnabled}
                  onChange={(_, checked) => {
                    setIsMaxLeafNodesEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        max_leaf_nodes: null,
                      });
                  }}
                />
              }
              label="Max Leaf Nodes Enabled"
            /> */}
            {/* <FormControlLabel
              control={
                <Checkbox
                  value={isClassWeightEnabled}
                  onChange={(_, checked) => {
                    setIsClassWeightEnabled(checked);
                    !checked &&
                      onParamsChange({
                        ...params,
                        class_weight: null,
                      });

                    checked && updateWeights();
                  }}
                />
              }
              label="Class Weight Enabled"
            /> */}
          </Box>
        </Box>
        {/* <Box
          sx={{
            display: "grid",
            gridTemplateRows: "repeat(2, max-content)",
          }}
        > */}
        {/* <FormControlLabel
            control={
              <Checkbox
                value={isMaxFeaturesFloat}
                onChange={(_, checked) => {
                  setIsMaxFeaturesFloat(checked);
                  !checked &&
                    onParamsChange({
                      ...params,
                      max_features: null,
                    });
                }}
              />
            }
            label="Is Max Features Numeric"
          /> */}

        {/* <FormControlLabel
            control={
              <Checkbox
                value={isClassWeightCustom}
                onChange={(_, checked) => {
                  setIsClassWeightCustom(checked);
                  onParamsChange({
                    ...params,
                    class_weight: checked ? {} : null,
                  });
                }}
              />
            }
            label="Is Class Weight Custom"
          /> */}
        {/* </Box> */}
      </Box>
      <Box
        sx={{
          display: "flex",
          gap: `${theme.spacing(2)} ${theme.spacing(1)}`,
          flexWrap: "wrap",
        }}
      >
        {/* {isMaxFeaturesFloat ? (
          <TextField
            sx={{ width: SELECTORS_WIDTH }}
            disabled={disabled || !isMaxFeaturesEnabled}
            label="Max Features"
            value={params.max_features || ""}
            onChange={(event) => {
              event.target.value.match(FloatRegexp) &&
                onParamsChange({
                  ...params,
                  max_features: event.target.value,
                });
            }}
            onBlur={(event) =>
              onParamsChange({
                ...params,
                max_features: CorrectFloat(event.target.value),
              })
            }
          />
        ) : (
          <FormControl sx={{ width: SELECTORS_WIDTH }}>
            <InputLabel>Max Feature</InputLabel>
            <Select
              disabled={disabled || !isMaxFeaturesEnabled}
              value={params.max_features || ""}
              label="Max Feature"
              onChange={(event) =>
                onParamsChange({
                  ...params,
                  max_features: event.target.value as DesicionMaxFeatures,
                })
              }
            >
              {values(DesicionMaxFeatures)?.map((x) => (
                <MenuItem key={x} value={x}>
                  {x}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )} */}

        {/* <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled || !isRandomStateEnabled}
          label="Random State"
          value={params.random_state || ""}
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
          disabled={disabled || !isMaxLeafNodesEnabled}
          label="Max Leaf Nodes"
          value={params.max_leaf_nodes || ""}
          onChange={(event) =>
            onParamsChange({
              ...params,
              max_leaf_nodes: Number(event.target.value),
            })
          }
          type="number"
        /> */}

        <TextField
          sx={{ width: SELECTORS_WIDTH }}
          disabled={disabled || !isMaxDepthEnabled}
          label="Max depth"
          value={params.max_depth || ""}
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
      {/* {isClassWeightCustom && isClassWeightEnabled ? (
        <Box
          sx={{
            mt: theme.spacing(4),
            gap: theme.spacing(2),
            display: "grid",
            width: "max-content",
            paddingRight: theme.spacing(4),
            borderRight: `2px solid ${theme.palette.info.main}`,
          }}
        >
          {entries(customClassWeights).map(([key, item]) => (
            <Box
              key={key}
              sx={{
                display: "grid",
                gap: theme.spacing(1),
                gridTemplateColumns: `repeat(2, ${SELECTORS_WIDTH}) 30px`,
              }}
            >
              <TextField
                sx={{ width: SELECTORS_WIDTH }}
                disabled={disabled}
                label="Label"
                value={item.label}
                onChange={(event) => {
                  setCustomClassWeights({
                    ...customClassWeights,
                    [key]: {
                      ...customClassWeights[key],
                      label: event.target.value,
                    },
                  });
                  updateWeights();
                }}
              />
              <TextField
                sx={{ width: SELECTORS_WIDTH }}
                disabled={disabled}
                label="Weight"
                value={item.value || ""}
                onChange={(event) => {
                  event.target.value.match(FloatRegexp) &&
                    setCustomClassWeights({
                      ...customClassWeights,
                      [key]: {
                        ...customClassWeights[key],
                        value: event.target.value,
                      },
                    });
                  updateWeights();
                }}
                onBlur={(event) => {
                  setCustomClassWeights({
                    ...customClassWeights,
                    [key]: {
                      ...customClassWeights[key],
                      value: event.target.value,
                    },
                  });
                  updateWeights();
                }}
              />
              <IconButton
                sx={{ width: "60px" }}
                onClick={() => {
                  setCustomClassWeights(omit(customClassWeights, [key]));
                  updateWeights();
                }}
              >
                <Delete />
              </IconButton>
            </Box>
          ))}
          <Button
            sx={{ mt: theme.spacing(1), width: "388px" }}
            variant="contained"
            onClick={() => {
              setCustomClassWeights({
                ...customClassWeights,
                [nanoid()]: { label: "", value: "0" },
              });
            }}
          >
            Добавить вес
          </Button>
        </Box>
      ) : (
        <FormControl sx={{ width: SELECTORS_WIDTH, mt: theme.spacing(2) }}>
          <InputLabel>Class Weight</InputLabel>
          <Select
            disabled={disabled || !isClassWeightEnabled}
            value={params.class_weight || ""}
            label="Class Weight"
            onChange={(event) =>
              onParamsChange({
                ...params,
                class_weight: event.target.value as DesicionClassWeight,
              })
            }
          >
            {values(DesicionClassWeight)?.map((x) => (
              <MenuItem key={x} value={x}>
                {x}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )} */}
    </Box>
  );
};

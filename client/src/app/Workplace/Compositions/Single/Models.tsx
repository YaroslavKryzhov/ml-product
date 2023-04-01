import { Box, Button, Divider, Typography } from "@mui/material";
import { UnavailableBlock } from "app/Workplace/common/UnavailableBlock";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { useCompositionInfoQuery } from "ducks/reducers/api/compositions.api";
import {
  addModel,
  changeCompositionType,
  changeDataframeId,
  changeParamsType,
  changeTestSize,
  setModels,
} from "ducks/reducers/compositions";
import { theme } from "globalStyle/theme";
import { isEmpty, keys } from "lodash";
import { useEffect } from "react";
import { batch } from "react-redux";
import { ModelProps } from "./ModelProps";
import { useParams } from "react-router-dom";

export const Models: React.FC<{ createMode?: boolean }> = ({ createMode }) => {
  const { models, customCompositionName } = useSESelector(
    (state) => state.compositions
  );

  const dispatch = useAppDispatch();
  const { compositionId } = useParams();

  const { data: modelData } = useCompositionInfoQuery(
    {
      model_id: compositionId!,
    },
    { skip: createMode || !compositionId }
  );

  useEffect(() => {
    batch(() => {
      modelData?.composition_params &&
        dispatch(setModels(modelData.composition_params));

      modelData?.composition_type &&
        dispatch(changeCompositionType("none" as any));

      modelData?.csv_name && dispatch(changeDataframeId(modelData.csv_id));

      modelData?.test_size && dispatch(changeTestSize(modelData.test_size));

      modelData?.params_type &&
        dispatch(changeParamsType(modelData.params_type));
    });
  }, [modelData]);

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(3) }} variant="h5">
        Модели
      </Typography>
      {keys(models).map((id) => (
        <ModelProps key={id} createMode={createMode} id={id} />
      ))}
      {createMode && (
        <>
          {isEmpty(models) && (
            <Box sx={{ mb: theme.spacing(4) }}>
              <UnavailableBlock label="Добавьте хотя бы одну модель" />
            </Box>
          )}
          <Button
            onClick={() => dispatch(addModel())}
            variant="contained"
            fullWidth
          >
            Добавить модель
          </Button>
        </>
      )}
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(2) }} />
    </Box>
  );
};

import { Box, Button, Divider, Typography } from "@mui/material";
import { UnavailableBlock } from "app/Workplace/common/UnavailableBlock";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { useCompositionInfoQuery } from "ducks/reducers/api/compositions.api";
import { addModel, setModels } from "ducks/reducers/compositions";
import { theme } from "globalStyle/theme";
import { isEmpty, keys } from "lodash";
import { useEffect } from "react";
import { ModelProps } from "./ModelProps";

export const Models: React.FC<{ createMode?: boolean }> = ({ createMode }) => {
  const { models, customCompositionName } = useSESelector(
    (state) => state.compositions
  );

  const dispatch = useAppDispatch();

  const { data: modelData } = useCompositionInfoQuery(
    {
      model_name: customCompositionName,
    },
    { skip: createMode }
  );

  useEffect(() => {
    modelData?.composition_params &&
      dispatch(setModels(modelData.composition_params));
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

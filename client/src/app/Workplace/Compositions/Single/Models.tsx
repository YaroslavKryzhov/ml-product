import { Box, Button, Divider, Typography } from "@mui/material";
import { UnavailableBlock } from "app/Workplace/common/UnavailableBlock";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { addModel } from "ducks/reducers/compositions";
import { theme } from "globalStyle/theme";
import { isEmpty, keys } from "lodash";
import { ModelProps } from "./ModelProps";

export const Models: React.FC<{ createMode?: boolean }> = ({ createMode }) => {
  const { models } = useSESelector((state) => state.compositions);
  const dispatch = useAppDispatch();

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Модели
      </Typography>
      {keys(models).map((id) => (
        <ModelProps createMode={createMode} id={id} />
      ))}
      {createMode && (
        <>
          {isEmpty(models) && (
            <Box sx={{ mb: theme.spacing(1) }}>
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

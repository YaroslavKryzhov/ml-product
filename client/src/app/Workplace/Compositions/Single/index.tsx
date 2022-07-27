import { Box, Button, Stack, Tooltip } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { isEmpty } from "lodash";
import React from "react";
import { CompositionProps } from "./CompositionProps";
import { Models } from "./Models";

export const CompositionSingle: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  const { taskType, compositionType, paramsType, documentName, models } =
    useSESelector((state) => state.compositions);

  const saveEnabled =
    taskType &&
    compositionType &&
    paramsType &&
    documentName &&
    !isEmpty(models);

  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}>
        <CompositionProps createMode={createMode} />
        <Models createMode={createMode} />
        {createMode && (
          <Tooltip
            followCursor
            disableHoverListener={Boolean(saveEnabled)}
            title="Заполните все обязательные поля и добавьте как минимум одну модель"
          >
            <Box>
              <Button
                disabled={!saveEnabled}
                onClick={() => {}}
                variant="contained"
                fullWidth
              >
                Создать
              </Button>
            </Box>
          </Tooltip>
        )}
      </Stack>
    </>
  );
};

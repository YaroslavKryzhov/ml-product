import { Box, Button, Divider, Stack, Tooltip } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import { useSESelector } from "ducks/hooks";
import { theme } from "globalStyle/theme";
import React from "react";
import { CompositionProps } from "./CompositionProps";

export const CompositionSingle: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  const { taskType, compositionType, paramsType, documentName } = useSESelector(
    (state) => state.compositions
  );

  const saveEnabled = taskType && compositionType && paramsType && documentName;

  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}>
        <CompositionProps createMode={createMode} />
        {createMode && (
          <>
            <Button onClick={() => {}} variant="contained" fullWidth>
              Добавить модель
            </Button>
            <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
          </>
        )}

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

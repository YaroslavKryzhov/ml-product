import { Box, Button, Stack, Tooltip } from "@mui/material";
import { nanoid } from "@reduxjs/toolkit";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import { useSESelector } from "ducks/hooks";
import { useTrainCompositionMutation } from "ducks/reducers/api/compositions.api";
import { entries, isEmpty } from "lodash";
import React from "react";
import { CompositionProps } from "./CompositionProps";
import { Models } from "./Models";

export const CompositionSingle: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  const {
    taskType,
    testSize,
    compositionType,
    paramsType,
    documentName,
    models,
  } = useSESelector((state) => state.compositions);

  const [train] = useTrainCompositionMutation();

  const saveEnabled =
    taskType &&
    compositionType &&
    paramsType &&
    documentName &&
    !isEmpty(models);

  const trainClick = () => {
    const convertedModels = entries(models).map(([_, model]) => model);

    train({
      body: convertedModels,
      params: {
        composition_type: compositionType!,
        params_type: paramsType!,
        document_name: documentName,
        model_name: nanoid(),
        test_size: testSize,
      },
    });
  };

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
                onClick={trainClick}
                variant="contained"
                fullWidth
              >
                Train
              </Button>
            </Box>
          </Tooltip>
        )}
      </Stack>
    </>
  );
};

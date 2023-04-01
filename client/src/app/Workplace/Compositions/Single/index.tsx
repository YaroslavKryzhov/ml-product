import { Box, Button, Stack, Tooltip } from "@mui/material";
import { pathify, useAppDispatch, useSESelector } from "ducks/hooks";
import { useTrainCompositionMutation } from "ducks/reducers/api/compositions.api";
import { resetComposition } from "ducks/reducers/compositions";
import { AppPage, WorkPage, DocumentPage } from "ducks/reducers/types";
import { entries, isEmpty } from "lodash";
import React from "react";
import { useNavigate, useParams } from "react-router";
import { CompositionMetrics } from "./CompositionMetrics";
import { CompositionProps } from "./CompositionProps";
import { Models } from "./Models";
import { Predict } from "./Predict";
import { WorkPageHeader } from "./WorkPageHeader";
import { addPendingTask } from "ducks/reducers/documents";

export const CompositionSingle: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  const {
    taskType,
    testSize,
    compositionType,
    paramsType,
    dataframeId,
    models,
    customCompositionName,
  } = useSESelector((state) => state.compositions);

  const { compositionId } = useParams();

  const dispatch = useAppDispatch();
  const [train] = useTrainCompositionMutation();
  const navigate = useNavigate();

  const saveEnabled =
    taskType &&
    compositionType &&
    paramsType &&
    dataframeId &&
    !isEmpty(models);

  const trainClick = () => {
    const convertedModels = entries(models).map(([_, model]) => model);

    const params = {
      task_type: taskType!,
      composition_type: compositionType!,
      params_type: paramsType!,
      dataframe_id: dataframeId!,
      model_name: customCompositionName,
      test_size: testSize,
    };

    train({
      body: convertedModels,
      params,
    });

    dispatch(addPendingTask(JSON.stringify(params)));

    navigate(
      pathify([AppPage.Workplace, WorkPage.Compositions, DocumentPage.List])
    );

    dispatch(resetComposition());
  };

  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}>
        <CompositionProps createMode={createMode} />
        {!createMode && <Predict model_id={compositionId!} />}
        {!createMode && compositionId && (
          <CompositionMetrics compositionId={compositionId} />
        )}
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

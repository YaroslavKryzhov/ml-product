import * as React from "react";
import Typography from "@mui/material/Typography";
import { Box, Paper, Skeleton, Stack, Tooltip } from "@mui/material";
import { theme } from "globalStyle/theme";
import { LoadingButton } from "@mui/lab";
import { CategoryMark, DocumentMethod } from "ducks/reducers/types";
import {
  useApplyDocMethodMutation,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { useParams } from "react-router-dom";
import { useCallback } from "react";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { useAppDispatch } from "ducks/hooks";
import { T } from "ramda";
import { ApplyMethodInfo } from "./ApplyMethodInfo";
import { ButtonsData, ButtonsGroupsLabels } from "./constants";
import { BtnGroups } from "./types";
import { UnavailableBlock } from "app/Workplace/common/UnavailableBlock";

export const DocumentMethods: React.FC = () => {
  const { docName } = useParams();
  const dispatch = useAppDispatch();

  const { data: infoData, isFetching: docInfoLoading } = useInfoDocumentQuery(
    docName!
  );
  const [applyMethod, { isLoading }] = useApplyDocMethodMutation();

  const setDialogApplyMethod = useCallback(
    (method: DocumentMethod) => {
      dispatch(
        setDialog({
          title: `Применение ${method}`,
          Content: <ApplyMethodInfo method={method} />,
          onAccept: async () => {
            dispatch(setDialogLoading(true));
            await applyMethod({ filename: docName!, function_name: method });
            dispatch(setDialogLoading(false));
          },
          onDismiss: T,
        })
      );
    },
    [dispatch, docName, applyMethod]
  );

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(3) }} variant="h5">
        Методы
      </Typography>

      {docInfoLoading ? (
        <Stack
          sx={{
            columnGap: theme.spacing(2),
            rowGap: theme.spacing(3),
            flexWrap: "wrap",
          }}
          direction="row"
        >
          <Skeleton
            variant="rectangular"
            width={`calc(25% - ${theme.spacing(2)})`}
            height={477}
          />
          <Skeleton
            variant="rectangular"
            width={`calc(25% - ${theme.spacing(2)})`}
            height={477}
          />
          <Skeleton
            variant="rectangular"
            width={`calc(25% - ${theme.spacing(2)})`}
            height={477}
          />
          <Skeleton variant="rectangular" width="25%" height={477} />
        </Stack>
      ) : (
        <>
          {infoData?.column_types ? (
            <Stack
              sx={{
                columnGap: theme.spacing(2),
                rowGap: theme.spacing(3),
                flexWrap: "wrap",
                justifyContent: "center",
              }}
              direction="row"
            >
              {Object.values(BtnGroups).map((groupKey) => {
                const isColumnsSelectForbidden =
                  groupKey === BtnGroups.group4 &&
                  !!infoData.column_types[CategoryMark.categorical]?.length;

                return (
                  <Paper
                    sx={{
                      backgroundColor: theme.palette.secondary.light,
                      padding: theme.spacing(3),
                      flexGrow: 1,
                      maxWidth: "33%",
                    }}
                    key={groupKey}
                    elevation={3}
                  >
                    <Typography
                      variant="h6"
                      sx={{ textAlign: "center", mb: theme.spacing(2) }}
                    >
                      {ButtonsGroupsLabels[groupKey]}
                    </Typography>

                    <Tooltip
                      followCursor
                      disableHoverListener={!isColumnsSelectForbidden}
                      title="Запрещено. Есть категориальные признаки."
                    >
                      <Stack
                        sx={{
                          gap: theme.spacing(1),
                          flexWrap: "wrap",
                        }}
                      >
                        {ButtonsData[groupKey].map((act) => (
                          <LoadingButton
                            disabled={isColumnsSelectForbidden}
                            loading={isLoading}
                            variant="contained"
                            key={act.value}
                            sx={{
                              flexGrow: 1,
                            }}
                            onClick={() => setDialogApplyMethod(act.value)}
                          >
                            {act.label}
                          </LoadingButton>
                        ))}
                      </Stack>
                    </Tooltip>
                  </Paper>
                );
              })}
            </Stack>
          ) : (
            <UnavailableBlock label="Методы доступны только после разметки" />
          )}
        </>
      )}
    </Box>
  );
};

import { Box, Button, Skeleton, Stack } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import { theme } from "globalStyle/theme";
import { pathify, useAppDispatch } from "ducks/hooks";
import DownloadIcon from "@mui/icons-material/Download";
import { useDeleteComposition } from "../Compositions/hooks";
import DeleteIcon from "@mui/icons-material/Delete";
import moment from "moment";
import { InfoChip } from "components/infoChip";
import { Size } from "app/types";
import { useLocation, useNavigate } from "react-router-dom";
import { CompositionPage } from "ducks/reducers/types";
import { EditableLabel } from "../common/styled";
import {
  useCompositionInfoQuery,
  useDownloadCompositionMutation,
  useRenameCompositionMutation,
} from "ducks/reducers/api/compositions.api";
import { changeCustomCompositionName } from "ducks/reducers/compositions";

export const CompositionsEntityHeader: React.FC<{
  initName?: string;
  worplacePage?: string;
}> = ({ initName }) => {
  const dispatch = useAppDispatch();
  const [editMode, setEditMode] = useState(false);
  const [customName, setCustomName] = useState(initName || "");
  const inputRef = useRef<HTMLLabelElement | null>(null);
  const [renameComposition] = useRenameCompositionMutation();

  const [downloadComp] = useDownloadCompositionMutation();
  const deleteComp = useDeleteComposition({ redirectAfter: true });

  const { pathname } = useLocation();
  const compositionPage = pathname.endsWith("create")
    ? CompositionPage.Create
    : CompositionPage.Single;

  const navigate = useNavigate();
  const onKeyDown = (e: React.KeyboardEvent<HTMLLabelElement>) => {
    if (e.code === "Enter") {
      e.preventDefault();
      (e.target as HTMLLabelElement).blur();
    }
    if (e.code === "Escape") {
      e.preventDefault();

      (e.target as HTMLLabelElement).blur();
    }
  };

  const { data: compData, isFetching: compInfoLoading } =
    useCompositionInfoQuery({ model_name: customName });

  useEffect(() => {
    editMode && inputRef.current?.focus();
  }, [editMode]);

  useEffect(() => {
    dispatch(changeCustomCompositionName(initName || ""));
  }, [initName]);

  const onRename = (e: React.FocusEvent<HTMLLabelElement>) => {
    const newName = e.target.innerText;
    setEditMode(false);

    if (compositionPage === CompositionPage.Single) {
      renameComposition({
        model_name: customName,
        new_model_name: newName,
      }).then(() => {
        setCustomName(newName);
        navigate(
          pathify([CompositionPage.List, newName], {
            changeLast: true,
          })
        );
      });
    }

    if (compositionPage === CompositionPage.Create) {
      dispatch(changeCustomCompositionName(newName));
    }
  };

  const isEdit = compositionPage === CompositionPage.Single;

  return (
    <Box>
      {isEdit && (
        <Stack direction="row" sx={{ gap: theme.spacing(2) }}>
          {compInfoLoading ? (
            <Skeleton variant="rectangular" width={215} height={22} />
          ) : (
            <InfoChip
              size={Size.small}
              label="Создано"
              info={
                compData &&
                moment(compData.create_date).format(theme.additional.timeFormat)
              }
            />
          )}
        </Stack>
      )}

      <Box
        sx={{
          mt: isEdit ? theme.spacing(3) : 0,
          display: "flex",
          justifyContent: "space-between",
          cursor: "pointer",
          "&:hover": { color: theme.palette.primary.light },
        }}
      >
        <Box>
          <Box onClick={() => !editMode && setEditMode(true)}>
            <EditableLabel
              ref={inputRef}
              editMode={editMode}
              onBlur={onRename}
              onKeyDown={onKeyDown}
              contentEditable={editMode}
            >
              {customName}
            </EditableLabel>

            <EditIcon
              onClick={() => setEditMode(!editMode)}
              sx={{
                ml: theme.spacing(1),
                verticalAlign: "middle",
                fontSize: theme.typography.h6.fontSize,
              }}
            />
          </Box>
        </Box>
        {isEdit && (
          <Stack
            direction="row"
            sx={{ gap: theme.spacing(1), height: "min-content" }}
          >
            <Button
              onClick={() => downloadComp({ model_name: customName })}
              variant="outlined"
              startIcon={<DownloadIcon />}
            >
              Скачать
            </Button>
            <Button
              onClick={() => deleteComp(customName)}
              variant="outlined"
              startIcon={<DeleteIcon />}
            >
              Удалить
            </Button>
          </Stack>
        )}
      </Box>
    </Box>
  );
};

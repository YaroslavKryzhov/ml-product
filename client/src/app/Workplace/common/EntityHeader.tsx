import { Box, Button, Skeleton, Stack } from "@mui/material";
import React, { useCallback, useEffect, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import { theme } from "globalStyle/theme";
import {
  useDownloadDocumentMutation,
  useInfoDocumentQuery,
  useRenameDocumentMutation,
} from "ducks/reducers/api/documents.api";
import { pathify, useAppDispatch } from "ducks/hooks";
import DownloadIcon from "@mui/icons-material/Download";
import { useDeleteFile } from "../Documents/hooks";
import DeleteIcon from "@mui/icons-material/Delete";
import moment from "moment";
import { InfoChip } from "components/infoChip";
import { Size } from "app/types";
import { useNavigate } from "react-router-dom";
import { CompositionPage, DocumentPage, WorkPage } from "ducks/reducers/types";
import { EditableLabel } from "./styled";
import { useRenameCompositionMutation } from "ducks/reducers/api/compositions.api";
import { changeCustomCompositionName } from "ducks/reducers/compositions";

export const EntityHeader: React.FC<{
  initName?: string;
  worplacePage?: string;
  compositionPage?: string;
}> = ({ initName, worplacePage, compositionPage }) => {
  const dispatch = useAppDispatch();
  const [editMode, setEditMode] = useState(false);
  const [customName, setCustomName] = useState(initName || "");
  const inputRef = useRef<HTMLLabelElement | null>(null);
  const [renameDoc] = useRenameDocumentMutation();
  const [renameComposition] = useRenameCompositionMutation();

  const [downloadDoc] = useDownloadDocumentMutation();
  const deleteDoc = useDeleteFile({ redirectAfter: true });
  const matchName =
    worplacePage === WorkPage.Documents
      ? customName.match(/(.*)(\.csv)/)
      : null;
  const navigate = useNavigate();
  const onKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLLabelElement>) => {
      if (e.code === "Enter") {
        e.preventDefault();
        (e.target as HTMLLabelElement).blur();
      }
      if (e.code === "Escape") {
        e.preventDefault();
        if (matchName) (e.target as HTMLLabelElement).innerText = matchName[1];
        (e.target as HTMLLabelElement).blur();
      }
    },
    [matchName]
  );

  const { data: docData, isFetching: docInfoLoading } =
    useInfoDocumentQuery(customName);

  useEffect(() => {
    editMode && inputRef.current?.focus();
  }, [editMode]);

  const onRename = useCallback(
    (e: React.FocusEvent<HTMLLabelElement>) => {
      const newName = e.target.innerText + (matchName && matchName[2]);
      setEditMode(false);

      if (worplacePage === WorkPage.Documents) {
        renameDoc({
          filename: customName,
          new_filename: newName,
        }).then(() => {
          setCustomName(newName);
          navigate(
            pathify([DocumentPage.List, newName], {
              changeLast: true,
            })
          );
        });
      }

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
    },
    [
      compositionPage,
      customName,
      dispatch,
      matchName,
      navigate,
      renameComposition,
      renameDoc,
      worplacePage,
    ]
  );

  const isEdit =
    worplacePage === WorkPage.Documents ||
    compositionPage === CompositionPage.Single;

  return (
    <Box>
      {isEdit && (
        <Stack direction="row" sx={{ gap: theme.spacing(2) }}>
          {docInfoLoading ? (
            <>
              <Skeleton variant="rectangular" width={215} height={22} />
              <Skeleton variant="rectangular" width={215} height={22} />
            </>
          ) : (
            <>
              <InfoChip
                size={Size.small}
                label="Загружено"
                info={
                  docData &&
                  moment(docData.upload_date).format(
                    theme.additional.timeFormat
                  )
                }
              />
              <InfoChip
                size={Size.small}
                label="Изменено"
                info={
                  docData &&
                  moment(docData.change_date).format(
                    theme.additional.timeFormat
                  )
                }
              />
            </>
          )}
        </Stack>
      )}

      <Box
        sx={{
          mt: theme.spacing(3),
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
              {matchName ? matchName[1] : customName}
            </EditableLabel>
            {matchName && (
              <EditableLabel editMode={editMode}>{matchName[2]}</EditableLabel>
            )}
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
              onClick={() => downloadDoc(customName)}
              variant="outlined"
              startIcon={<DownloadIcon />}
            >
              Скачать
            </Button>
            <Button
              onClick={() => deleteDoc(customName)}
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

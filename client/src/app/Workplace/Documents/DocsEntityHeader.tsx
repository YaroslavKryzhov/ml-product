import { Box, Button, Skeleton, Stack } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import { theme } from "globalStyle/theme";
import {
  useDownloadDocumentMutation,
  useInfoDocumentQuery,
  useRenameDocumentMutation,
} from "ducks/reducers/api/documents.api";
import DownloadIcon from "@mui/icons-material/Download";
import { useDeleteFile } from "./hooks";
import DeleteIcon from "@mui/icons-material/Delete";
import moment from "moment";
import { InfoChip } from "components/infoChip";
import { Size } from "app/types";
import { EditableLabel } from "../common/styled";

export const DocsEntityHeader: React.FC<{
  docId: string;
  worplacePage?: string;
}> = ({ docId }) => {
  const [editMode, setEditMode] = useState(false);
  const [customName, setCustomName] = useState("");
  const inputRef = useRef<HTMLLabelElement | null>(null);
  const { data: documentData } = useInfoDocumentQuery(docId);
  const [renameDoc] = useRenameDocumentMutation();

  const [downloadDoc] = useDownloadDocumentMutation();
  const deleteDoc = useDeleteFile({ redirectAfter: true });
  const matchName = customName.match(/(.*)(\.csv)/);

  useEffect(() => {
    setCustomName(documentData?.filename || "");
  }, [documentData?.filename]);

  const onKeyDown = (e: React.KeyboardEvent<HTMLLabelElement>) => {
    if (e.code === "Enter") {
      e.preventDefault();
      (e.target as HTMLLabelElement).blur();
    }
    if (e.code === "Escape") {
      e.preventDefault();
      if (matchName) (e.target as HTMLLabelElement).innerText = matchName[1];
      (e.target as HTMLLabelElement).blur();
    }
  };

  const { data: docData, isFetching: docInfoLoading } =
    useInfoDocumentQuery(docId);

  useEffect(() => {
    editMode && inputRef.current?.focus();
  }, [editMode]);

  const onRename = (e: React.FocusEvent<HTMLLabelElement>) => {
    const newName = e.target.innerText + (matchName && matchName[2]);
    setEditMode(false);

    renameDoc({
      dataframe_id: docId,
      new_filename: newName,
    }).then(() => setCustomName(newName));
  };

  return (
    <Box>
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
                moment(docData.created_at).format(theme.additional.timeFormat)
              }
            />
            <InfoChip
              size={Size.small}
              label="Изменено"
              info={
                docData &&
                moment(docData.updated_at).format(theme.additional.timeFormat)
              }
            />
          </>
        )}
      </Stack>

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

        <Stack
          direction="row"
          sx={{ gap: theme.spacing(1), height: "min-content" }}
        >
          <Button
            onClick={() =>
              downloadDoc({
                dataframe_id: docId,
                filename: customName,
              })
            }
            variant="outlined"
            startIcon={<DownloadIcon />}
          >
            Скачать
          </Button>
          <Button
            onClick={() => deleteDoc(customName, docId)}
            variant="outlined"
            startIcon={<DeleteIcon />}
          >
            Удалить
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};

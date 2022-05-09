import { Box, Button } from "@mui/material";
import React, { useCallback, useEffect, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import { theme } from "globalStyle/theme";
import styled from "@emotion/styled";
import { useRenameDocumentMutation } from "ducks/reducers/api/documents.api";
import PreviewIcon from "@mui/icons-material/Preview";
import { useAppDispatch } from "ducks/hooks";
import { DocumentPreview } from "./DocumentPreview";
import { setDialog } from "ducks/reducers/dialog";

const EditableLabel = styled.label<{ editMode?: boolean }>`
  &:focus-visible {
    outline: none;
  }
  ${({ editMode }) =>
    editMode &&
    `border-bottom: ${theme.additional.borderWidth}px solid ${theme.palette.primary.main};`}
`;

export const DocHeader: React.FC<{ initName: string }> = ({ initName }) => {
  const [editMode, setEditMode] = useState(false);
  const [customName, setCustomName] = useState(initName);
  const inputRef = useRef<HTMLLabelElement | null>(null);
  const [rename] = useRenameDocumentMutation();
  const dispatch = useAppDispatch();
  const matchName = customName.match(/(.*)(\.csv)/);
  const onKeyDown = useCallback((e: React.KeyboardEvent<HTMLLabelElement>) => {
    if (e.code === "Enter") {
      e.preventDefault();
      (e.target as HTMLLabelElement).blur();
    }
  }, []);

  useEffect(() => {
    editMode && inputRef.current?.focus();
  }, [editMode]);

  const setDialogProps = useCallback(() => {
    dispatch(
      setDialog({
        title: "Просмотр",
        Content: <DocumentPreview docName={customName} />,
        onDismiss: () => {},
        dismissText: "Закрыть",
      })
    );
  }, []);

  if (!matchName) return <>{customName}</>;

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        cursor: "pointer",
        "&:hover": { color: theme.palette.primary.light },
      }}
    >
      <Box onClick={() => !editMode && setEditMode(true)}>
        <EditableLabel
          ref={inputRef}
          editMode={editMode}
          onBlur={(e) => {
            const newName = e.target.innerText + matchName[2];
            rename({ filename: customName, new_filename: newName });
            setCustomName(newName);
            setEditMode(false);
          }}
          onKeyDown={onKeyDown}
          contentEditable={editMode}
        >
          {matchName[1]}
        </EditableLabel>
        <EditableLabel editMode={editMode}>{matchName[2]}</EditableLabel>
        <EditIcon
          onClick={() => setEditMode(!editMode)}
          sx={{
            ml: theme.spacing(1),
            verticalAlign: "middle",
            fontSize: theme.typography.h6.fontSize,
          }}
        />
      </Box>
      <Button
        onClick={setDialogProps}
        variant="outlined"
        startIcon={<PreviewIcon />}
      >
        Просмотр
      </Button>
    </Box>
  );
};

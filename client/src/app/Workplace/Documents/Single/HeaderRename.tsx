import { Box } from "@mui/material";
import React, { useCallback, useEffect, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import { theme } from "globalStyle/theme";
import styled from "@emotion/styled";
import { useRenameDocumentMutation } from "ducks/reducers/api/documents.api";

const EditableLabel = styled.label<{ editMode?: boolean }>`
  &:focus-visible {
    outline: none;
  }
  ${({ editMode }) =>
    editMode &&
    `border-bottom: ${theme.additional.borderWidth}px solid ${theme.palette.primary.main};`}
`;

export const HeaderRename: React.FC<{ initName: string }> = ({ initName }) => {
  const [editMode, setEditMode] = useState(false);
  const [customName, setCustomName] = useState(initName);
  const inputRef = useRef<HTMLLabelElement | null>(null);
  const [rename] = useRenameDocumentMutation();
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

  if (!matchName) return <>{customName}</>;

  return (
    <Box
      sx={{
        cursor: "pointer",
        "&:hover": { color: theme.palette.primary.light },
        width: "fit-content",
      }}
      onClick={() => !editMode && setEditMode(true)}
    >
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
  );
};

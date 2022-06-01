import { Box, TextField, Typography } from "@mui/material";
import { CenteredContainer, helperTextProps } from "components/muiOverride";
import { theme } from "globalStyle/theme";
import React, { useCallback, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { first } from "lodash";
import AttachmentIcon from "@mui/icons-material/Attachment";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  changeCustomFileName,
  changeSelectedFile,
} from "ducks/reducers/documents";
import { setDialogAcceptDisabled } from "ducks/reducers/dialog";
import { SnackBarType, useNotice } from "app/Workplace/common/useNotice";

export const DocumentDrop: React.FC = () => {
  const { customFileName, selectedFile } = useSESelector(
    (state) => state.documents
  );
  const dispatch = useAppDispatch();

  const showTypeError = useNotice({
    label: "Разрешены только CSV файлы",
    type: SnackBarType.error,
  });

  const onDropAccepted = useCallback((files: File[]) => {
    const file = first(files);
    if (file) {
      dispatch(changeSelectedFile(file));
      dispatch(changeCustomFileName(file.name));
    }
  }, []);

  const onDropRejected = useCallback(
    () => showTypeError(true),
    [showTypeError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDropAccepted,
    onDropRejected,
    accept: {
      "application/vnd.ms-excel": [".csv"],
      "text/plain": [".csv"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".csv",
      ],
    },
    maxFiles: 1,
  });
  const { ref, ...rootProps } = getRootProps();

  const nameError = !!selectedFile
    ? !customFileName
      ? "Обязательное поле"
      : !/.csv$/g.test(customFileName)
      ? "Расширение должно быть .csv"
      : null
    : null;

  useEffect(() => {
    dispatch(setDialogAcceptDisabled(!(selectedFile && !nameError)));
  }, [selectedFile, customFileName]);

  return (
    <Box sx={{ mt: theme.spacing(1) }}>
      <TextField
        disabled={!selectedFile}
        size="small"
        label="Название файла"
        value={customFileName}
        onChange={(e) => dispatch(changeCustomFileName(e.target.value))}
        sx={{ mb: theme.spacing(2) }}
        helperText={nameError || " "}
        error={!!nameError}
        FormHelperTextProps={helperTextProps}
        fullWidth
      />
      <CenteredContainer
        {...rootProps}
        sx={{
          height: 80,
          width: 400,
          textAlign: "center",
          border: `${theme.additional.borderWidth}px dashed ${
            isDragActive || selectedFile
              ? theme.palette.primary.dark
              : theme.palette.secondary.dark
          }`,
          borderRadius: `${theme.shape.borderRadius}px`,
          p: theme.spacing(2),
          color:
            isDragActive || selectedFile
              ? theme.palette.primary.dark
              : theme.palette.secondary.dark,
          cursor: "pointer",
          "&:hover": {
            borderColor: theme.palette.primary.light,
            color: theme.palette.primary.light,
          },
        }}
      >
        <input {...getInputProps()} />
        {selectedFile ? (
          <AttachmentIcon sx={{ fontSize: theme.typography.h4 }} />
        ) : (
          <Typography variant="body2">
            Перетащите файл сюда или нажмите, чтобы выбрать (только CSV)
          </Typography>
        )}
      </CenteredContainer>
    </Box>
  );
};

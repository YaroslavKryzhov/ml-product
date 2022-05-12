import {
  Box,
  Slide,
  SlideProps,
  Snackbar,
  TextField,
  Typography,
} from "@mui/material";
import { CenteredContainer, helperTextProps } from "components/muiOverride";
import { theme } from "globalStyle/theme";
import React, { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { first } from "lodash";
import AttachmentIcon from "@mui/icons-material/Attachment";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  changeCustomFileName,
  changeSelectedFile,
} from "ducks/reducers/documents";
import { setDialogAcceptDisabled } from "ducks/reducers/dialog";
import { SlideTr } from "app/Workplace/common/styled";

export const DocumentDrop: React.FC = () => {
  const { customFileName, selectedFile } = useSESelector(
    (state) => state.documents
  );
  const [errorNoticeOpened, setErrorNoticeOpened] = useState<boolean>(false);
  const dispatch = useAppDispatch();

  const onDropAccepted = useCallback((files: File[]) => {
    const file = first(files);
    if (file) {
      dispatch(changeSelectedFile(file));
      dispatch(changeCustomFileName(file.name));
    }
  }, []);

  const onDropRejected = useCallback(
    () => setErrorNoticeOpened(true),

    []
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
      <Snackbar
        autoHideDuration={3000}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        open={errorNoticeOpened}
        onClose={() => setErrorNoticeOpened(false)}
        message={
          <Typography variant="body2" sx={{ color: theme.palette.error.main }}>
            Разрешены только CSV файлы
          </Typography>
        }
        TransitionComponent={SlideTr}
      />
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

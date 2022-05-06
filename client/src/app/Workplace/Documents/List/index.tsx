import { Box, Button } from "@mui/material";
import { nanoid } from "@reduxjs/toolkit";
import { MenuContext } from "app/Workplace";
import { TableFix } from "app/Workplace/common/Table";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  useAllDocumentsQuery,
  usePostDocumentMutation,
} from "ducks/reducers/api/documents.api";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import {
  changeCustomFileName,
  changeSelectedFile,
} from "ducks/reducers/documents";
import { store } from "ducks/store";
import { theme } from "globalStyle/theme";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { DocumentDrop } from "./DropFileDialog";

const columns = [
  {
    Header: "Название",
    accessor: "name",
  },
  {
    Header: "Загружено",
    accessor: "upload_date",
  },
  {
    Header: "Изменено",
    accessor: "change_date",
  },
];

export const DocumentsList: React.FC = () => {
  const { data: allDocuments } = useAllDocumentsQuery();
  const { menuOpened } = useContext(MenuContext);
  const [forceResize, setForceResize] = useState("");
  const { customFileName, selectedFile } = useSESelector(
    (state) => state.documents
  );
  const dispatch = useAppDispatch();
  const [postDoc] = usePostDocumentMutation();

  useEffect(() => {
    const interval = setInterval(() => setForceResize(nanoid()), 0);

    setTimeout(
      () => clearInterval(interval),
      theme.transitions.duration.complex
    );

    return () => clearInterval(interval);
  }, [menuOpened]);

  const setDialogProps = useCallback(() => {
    dispatch(
      setDialog({
        title: "Загрузка файла",
        Content: <DocumentDrop />,
        onAccept: async () => {
          const { customFileName, selectedFile } = store.getState().documents;
          if (!selectedFile) return;
          dispatch(setDialogLoading(true));
          await postDoc({
            filename: customFileName,
            file: selectedFile,
          });
          dispatch(setDialogLoading(false));
        },
        acceptDisabled: true,
        onClose: () => {
          dispatch(changeCustomFileName(""));
          dispatch(changeSelectedFile(null));
        },

        acceptText: "Загрузить",
        dismissText: "Отменить",
      })
    );
  }, []);

  return (
    <Box>
      <Button
        onClick={setDialogProps}
        variant="contained"
        fullWidth
        sx={{ mb: theme.spacing(2) }}
      >
        Загрузить CSV
      </Button>
      <TableFix
        forceResize={forceResize}
        resizable
        data={allDocuments || []}
        columns={columns}
        sortBy={[
          { id: columns[2].accessor, desc: true },
          { id: columns[0].accessor, desc: true },
          { id: columns[1].accessor, desc: true },
        ]}
      />
    </Box>
  );
};

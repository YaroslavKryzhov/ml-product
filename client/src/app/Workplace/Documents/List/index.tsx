import { Box, Button } from "@mui/material";
import { nanoid } from "@reduxjs/toolkit";
import { MenuContext } from "app/Workplace";
import { compareDate, TableFix } from "app/Workplace/common/Table";
import { useAppDispatch } from "ducks/hooks";
import {
  documentsApi,
  useAllDocumentsQuery,
  useDeleteDocumentMutation,
  usePostDocumentMutation,
} from "ducks/reducers/api/documents.api";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import {
  changeCustomFileName,
  changeDocumentPage,
  changeSelectedFile,
} from "ducks/reducers/documents";
import { store } from "ducks/store";
import { theme } from "globalStyle/theme";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { DocumentDrop } from "./DropFileDialog";
import moment from "moment";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { ActionIconSx } from "app/Workplace/common/Table/components/Body";
import { DocumentPage } from "ducks/reducers/types";

enum Columns {
  upload = "upload_date",
  change = "change_date",
  name = "name",
}

const columns = [
  {
    Header: "Название",
    accessor: Columns.name,
  },
  {
    Header: "Загружено",
    accessor: Columns.upload,
    sortType: compareDate(Columns.upload),
  },
  {
    Header: "Изменено",
    accessor: Columns.change,
    sortType: compareDate(Columns.change),
  },
];

export const DocumentsList: React.FC = () => {
  const { data: allDocuments } = useAllDocumentsQuery();
  const { menuOpened } = useContext(MenuContext);
  const [forceResize, setForceResize] = useState("");
  const dispatch = useAppDispatch();
  const [postDoc] = usePostDocumentMutation();
  const [deleteDoc] = useDeleteDocumentMutation();

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

  const convertedData = useMemo(
    () =>
      allDocuments?.map((x) => ({
        ...x,
        upload_date: moment(x.upload_date).format(theme.additional.timeFormat),
        change_date: moment(x.change_date).format(theme.additional.timeFormat),
      })) || [],
    [allDocuments]
  );

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
        rowActions={[
          {
            name: "Edit",
            icon: <EditIcon sx={ActionIconSx} />,
            onClick: (row) => {
              documentsApi.util.updateQueryData(
                "infoDocument",
                row.values.name,
                (draft) => (draft.name = row.values.name)
              );

              dispatch(changeDocumentPage(DocumentPage.Single));
            },
          },
          {
            name: "Delete",
            icon: <DeleteIcon sx={{ ActionIconSx }} />,
            onClick: (row) =>
              dispatch(
                setDialog({
                  title: "Удаление",
                  text: `Вы действительно хотите удалить файл ${
                    row.values[Columns.name]
                  }?`,
                  onAccept: async () => {
                    dispatch(setDialogLoading(true));
                    await deleteDoc(row.values[Columns.name]);
                    dispatch(setDialogLoading(false));
                  },
                })
              ),
          },
        ]}
        rowHoverable
        forceResize={forceResize}
        resizable
        data={convertedData}
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

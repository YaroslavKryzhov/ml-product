import { Box, Button, Skeleton } from "@mui/material";
import { compareDate, TableFix } from "components/Table";
import { pathify, useAppDispatch } from "ducks/hooks";
import {
  useAllDocumentsQuery,
  useDownloadDocumentMutation,
  usePostDocumentMutation,
} from "ducks/reducers/api/documents.api";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import {
  changeCustomFileName,
  changeSelectedFile,
} from "ducks/reducers/documents";
import { store } from "ducks/store";
import { theme } from "globalStyle/theme";
import React from "react";
import { DocumentDrop } from "./DropFileDialog";
import moment from "moment";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { ActionIconSx } from "components/Table/components/Body";
import { useNavigate } from "react-router-dom";
import DownloadIcon from "@mui/icons-material/Download";
import { useDeleteFile } from "../hooks";
import { addNotice, SnackBarType } from "ducks/reducers/notices";
import { WorkPageHeader } from "../Single/WorkPageHeader";

enum Columns {
  upload = "upload_date",
  change = "change_date",
  filename = "filename",
}

const columns = [
  {
    Header: "Название",
    accessor: Columns.filename,
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
  const { data: allDocuments, isFetching } = useAllDocumentsQuery();

  const dispatch = useAppDispatch();
  const [postDoc] = usePostDocumentMutation();
  const [downloadDoc] = useDownloadDocumentMutation();
  const deleteDoc = useDeleteFile();
  const navigate = useNavigate();

  const noticeSuccess = () =>
    dispatch(
      addNotice({
        label: "Файл успешно загружен",
        type: SnackBarType.success,
        id: Date.now(),
      })
    );

  const setDialogProps = () => {
    dispatch(
      setDialog({
        title: "Загрузка файла",
        Content: <DocumentDrop />,
        onAccept: async () => {
          const { customFileName, selectedFile } = store.getState().documents;
          if (!selectedFile) return;
          dispatch(setDialogLoading(true));
          postDoc({
            filename: customFileName,
            file: selectedFile,
          })
            .unwrap()
            .then(noticeSuccess)
            .catch((err) => {
              err?.originalStatus === 200 && noticeSuccess();

              err.status === 422 &&
                dispatch(
                  addNotice({
                    label: "Файл с таким именем уже существует.",
                    type: SnackBarType.error,
                    id: Date.now(),
                  })
                );
            })
            .finally(() => dispatch(setDialogLoading(false)));
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
  };

  const convertedData =
    allDocuments?.map((x) => ({
      ...x,
      upload_date: moment(x.created_at).format(theme.additional.timeFormat),
      change_date: moment(x.updated_at).format(theme.additional.timeFormat),
    })) || [];

  return (
    <>
      <WorkPageHeader />
      <Box>
        <Button
          onClick={setDialogProps}
          variant="contained"
          fullWidth
          sx={{ mb: theme.spacing(2) }}
        >
          Загрузить CSV
        </Button>
        {isFetching ? (
          <Skeleton variant="rectangular" width="100%" height={700} />
        ) : (
          <TableFix
            rowActions={[
              {
                name: "Редактировать",
                icon: <EditIcon sx={ActionIconSx} />,
                onClick: (row) => {
                  navigate(
                    pathify([(row.original as any).id], { relative: true })
                  );
                },
              },
              {
                name: "Скачать",
                icon: <DownloadIcon sx={ActionIconSx} />,
                onClick: (row) =>
                  downloadDoc({
                    dataframe_id: (row.original as any).id,
                    filename: row.values[Columns.filename],
                  }),
              },
              {
                name: "Удалить",
                icon: <DeleteIcon sx={{ ActionIconSx }} />,
                onClick: (row) =>
                  deleteDoc(
                    row.values[Columns.filename],
                    (row.original as any).id
                  ),
              },
            ]}
            rowHoverable
            forceResize
            resizable
            data={convertedData}
            columns={columns}
            sortBy={[
              { id: columns[2].accessor, desc: true },
              { id: columns[0].accessor, desc: true },
              { id: columns[1].accessor, desc: true },
            ]}
          />
        )}
      </Box>
    </>
  );
};

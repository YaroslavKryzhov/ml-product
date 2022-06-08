import { Box, Button, Skeleton } from "@mui/material";
import { compareDate, TableFix } from "app/Workplace/common/Table";
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
import React, { useCallback, useMemo } from "react";
import { DocumentDrop } from "./DropFileDialog";
import moment from "moment";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { ActionIconSx } from "app/Workplace/common/Table/components/Body";
import { useNavigate } from "react-router-dom";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import DownloadIcon from "@mui/icons-material/Download";
import { useDeleteFile } from "../hooks";
import { addNotice, SnackBarType } from "ducks/reducers/notices";
import { StandardResponseData } from "ducks/reducers/types";

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
  const { data: allDocuments, isFetching } = useAllDocumentsQuery();

  const dispatch = useAppDispatch();
  const [postDoc] = usePostDocumentMutation();
  const [downloadDoc] = useDownloadDocumentMutation();
  const deleteDoc = useDeleteFile();
  const navigate = useNavigate();

  const setDialogProps = useCallback(() => {
    dispatch(
      setDialog({
        title: "Загрузка файла",
        Content: <DocumentDrop />,
        onAccept: async () => {
          const { customFileName, selectedFile } = store.getState().documents;
          if (!selectedFile) return;
          dispatch(setDialogLoading(true));
          const res = (await postDoc({
            filename: customFileName,
            file: selectedFile,
          })) as StandardResponseData;
          dispatch(setDialogLoading(false));

          if (res.data.status_code === 200) {
            dispatch(
              addNotice({
                label: "Файл успешно загружен",
                type: SnackBarType.success,
                id: Date.now(),
              })
            );
          }

          if (res.data.status_code === 409) {
            dispatch(
              addNotice({
                label: "Файл с таким именем уже существует",
                type: SnackBarType.error,
                id: Date.now(),
              })
            );
          }
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
                  navigate(pathify([row.values.name], { relative: true }));
                },
              },
              {
                name: "Скачать",
                icon: <DownloadIcon sx={ActionIconSx} />,
                onClick: (row) => {
                  downloadDoc(row.values[Columns.name]);
                },
              },
              {
                name: "Удалить",
                icon: <DeleteIcon sx={{ ActionIconSx }} />,
                onClick: (row) => deleteDoc(row.values[Columns.name]),
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

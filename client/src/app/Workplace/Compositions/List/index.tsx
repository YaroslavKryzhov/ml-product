import { Box, Button, Skeleton } from "@mui/material";
import { compareDate, TableFix } from "components/Table";
import { pathify, useAppDispatch } from "ducks/hooks";
import { theme } from "globalStyle/theme";
import React, { useMemo } from "react";
import moment from "moment";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { ActionIconSx } from "components/Table/components/Body";
import { useNavigate } from "react-router-dom";
import DownloadIcon from "@mui/icons-material/Download";
import {
  useAllCompositionsQuery,
  useDownloadCompositionMutation,
} from "ducks/reducers/api/compositions.api";
import { AppPage, CompositionPage, WorkPage } from "ducks/reducers/types";
import { resetComposition } from "ducks/reducers/compositions";
import { WorkPageHeader } from "../Single/WorkPageHeader";
import { useDeleteComposition } from "../hooks";

enum Columns {
  create = "create_date",
  status = "status",
  filename = "filename",
  taskType = "task_type",
  compositionType = "composition_type",
}

const columns = [
  {
    Header: "Название",
    accessor: Columns.filename,
  },
  {
    Header: "Загружено",
    accessor: Columns.create,
    sortType: compareDate(Columns.create),
  },
  {
    Header: "Статус",
    accessor: Columns.status,
  },
  {
    Header: "Задача",
    accessor: Columns.taskType,
  },
  {
    Header: "Тип",
    accessor: Columns.compositionType,
  },
];

export const CompositionsList: React.FC = () => {
  const { data: allCompositions, isFetching } = useAllCompositionsQuery();

  const [downloadCompositions] = useDownloadCompositionMutation();
  const deleteComp = useDeleteComposition({ redirectAfter: true });

  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const convertedData = useMemo(
    () =>
      allCompositions?.map((x) => ({
        ...x,
        create_date: moment(x.create_date).format(theme.additional.timeFormat),
      })) || [],
    [allCompositions]
  );

  return (
    <>
      <WorkPageHeader />
      <Box>
        <Button
          onClick={() => {
            dispatch(resetComposition());
            navigate(
              pathify([
                AppPage.Workplace,
                WorkPage.Compositions,
                CompositionPage.Create,
              ])
            );
          }}
          variant="contained"
          fullWidth
          sx={{ mb: theme.spacing(2) }}
        >
          Создать композицию
        </Button>
        {isFetching ? (
          <Skeleton variant="rectangular" width="100%" height={700} />
        ) : (
          <TableFix
            compactFromPx={600}
            offHeaderPaddingsFrom={600}
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
                onClick: (row) => {
                  downloadCompositions({
                    model_name: row.values[Columns.filename],
                    model_id: (row.original as any).id,
                  });
                },
              },
              {
                name: "Удалить",
                icon: <DeleteIcon sx={{ ActionIconSx }} />,
                onClick: (row) =>
                  deleteComp(
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
              { id: columns[0].accessor, desc: true },
              { id: columns[1].accessor, desc: true },
            ]}
          />
        )}
      </Box>
    </>
  );
};

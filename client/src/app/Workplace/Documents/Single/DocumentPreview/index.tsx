import { TableFix } from "app/Workplace/common/Table";
import {
  useColumnMarksDocumentQuery,
  useColumnsStatsDocumentQuery,
  useDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import React, { useMemo, useState } from "react";
import { zipObject, unzip, values, keys, entries, first } from "lodash";
import {
  CategoryMark,
  DocumentStatsInfo,
  PandasInfoColumns,
} from "ducks/reducers/types";
import { BallTriangle } from "react-loader-spinner";
import { theme } from "globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";
import { Box, Pagination } from "@mui/material";
import { Fixed } from "app/Workplace/common/Table/types";
import { HeaderCell } from "./HeaderCell";

const convertData = (data: Record<string, string | number>) =>
  unzip(values(data).map((x) => values(x as any))).map((zipArr) =>
    zipObject(keys(data), zipArr)
  );

const findFieldInInfo = (
  info: DocumentStatsInfo,
  field: PandasInfoColumns,
  column: string
) => {
  const columnInx = info.column_name.findIndex((x) => x === column);

  return info[field][columnInx];
};

export const DocumentPreview: React.FC<{ docName: string }> = ({ docName }) => {
  const [page, setPage] = useState<number>(1);
  const { data, isLoading } = useDocumentQuery({ filename: docName, page });
  const { data: infoData } = useInfoStatsDocumentQuery(docName);
  const { data: columnsStats } = useColumnsStatsDocumentQuery(docName);
  const { data: columnMarks } = useColumnMarksDocumentQuery(docName);

  const convertedData = useMemo(
    () => (data?.records ? convertData(data.records) : []),
    [data]
  );

  const columns = useMemo(
    () =>
      data?.records && infoData && columnsStats
        ? Object.keys(data.records).map((x, inx, arr) => ({
            accessor: x,
            fixed: inx === arr.length - 1 ? Fixed.right : Fixed.left,
            Header: (
              <HeaderCell
                type={
                  first(
                    entries(columnMarks).find(
                      ([_, values]) => values.includes(x) || x === values
                    )
                  ) as CategoryMark
                }
                right={inx === arr.length - 1}
                name={x}
                notNullNum={findFieldInInfo(
                  infoData,
                  PandasInfoColumns.nonNullCount,
                  x
                )}
                dType={findFieldInInfo(infoData, PandasInfoColumns.dataType, x)}
                columnData={columnsStats.find((col) => col.name === x)!}
              />
            ),
          }))
        : [],
    [data, infoData, columnsStats]
  );

  if (isLoading)
    return (
      <CenteredContainer sx={{ width: "100vw", height: "calc(100vh - 200px)" }}>
        <BallTriangle
          color={theme.palette.primary.main}
          width={theme.typography.h1.fontSize}
          height={theme.typography.h1.fontSize}
        />
      </CenteredContainer>
    );

  return (
    <Box>
      <TableFix
        compact
        offHeaderPaddings
        defaultColumnSizing={{ minWidth: 70 }}
        forceResize
        resizable
        data={convertedData}
        columns={columns}
        tableMaxHeight="500px"
      />
      <Pagination
        sx={{ mt: theme.spacing(2) }}
        page={page}
        onChange={(_, page) => setPage(page)}
        count={data?.total}
        variant="outlined"
        shape="rounded"
      />
    </Box>
  );
};

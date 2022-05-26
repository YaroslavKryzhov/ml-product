import { TableFix } from "app/Workplace/common/Table";
import {
  useColumnMarksDocumentQuery,
  useColumnsStatsDocumentQuery,
  useDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import React, { useCallback, useMemo, useState } from "react";
import { zipObject, unzip, values, keys, entries, first } from "lodash";
import {
  CategoryMark,
  ColumnStats,
  DocumentStatsInfo,
  PandasInfoColumns,
} from "ducks/reducers/types";
import { BallTriangle } from "react-loader-spinner";
import { theme } from "globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";
import { Box, Pagination } from "@mui/material";
import { Fixed } from "app/Workplace/common/Table/types";
import { HeaderCell } from "./HeaderCell";
import { useParams } from "react-router-dom";

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

export const DocumentPreview: React.FC = () => {
  const { docName } = useParams();
  const [page, setPage] = useState<number>(1);
  const { data } = useDocumentQuery({ filename: docName!, page });
  const { data: infoData } = useInfoStatsDocumentQuery(docName!);
  const { data: columnsStats } = useColumnsStatsDocumentQuery(docName!);
  const { data: columnMarks } = useColumnMarksDocumentQuery(docName!);

  const convertedData = useMemo(
    () => (data?.records ? convertData(data.records) : []),
    [data]
  );

  const getHeaderType = useCallback(
    (val: string) =>
      (first(
        entries(columnMarks).find(
          ([_, values]) => values.includes(val) || val === values
        )
      ) as CategoryMark) || null,
    [columnMarks]
  );

  const getHeaderNotNull = useCallback(
    (val: string) =>
      infoData
        ? findFieldInInfo(infoData, PandasInfoColumns.nonNullCount, val)
        : null,
    [infoData]
  );

  const getHeaderDType = useCallback(
    (val: string) =>
      infoData
        ? findFieldInInfo(infoData, PandasInfoColumns.dataType, val)
        : null,
    [infoData]
  );

  const getHeaderColumnsData = useCallback(
    (val: string) =>
      columnsStats ? columnsStats.find((col) => col.name === val)! : null,
    [columnsStats]
  );

  const columns = useMemo(
    () =>
      data?.records
        ? Object.keys(data.records).map((x, inx, arr) => ({
            accessor: x,
            fixed: inx === arr.length - 1 ? Fixed.right : Fixed.left,
            Header: (
              <HeaderCell
                type={getHeaderType(x)}
                right={inx === arr.length - 1}
                name={x}
                notNullNum={getHeaderNotNull(x)}
                dType={getHeaderDType(x)}
                columnData={getHeaderColumnsData(x)}
              />
            ),
          }))
        : [],
    [
      data,
      getHeaderColumnsData,
      getHeaderNotNull,
      getHeaderDType,
      getHeaderType,
    ]
  );

  return (
    <Box>
      <TableFix
        compact
        offHeaderPaddings
        defaultColumnSizing={{ minWidth: 135 }}
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

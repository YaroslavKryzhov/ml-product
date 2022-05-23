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
import { Box, Pagination, Typography } from "@mui/material";
import { Fixed } from "app/Workplace/common/Table/types";
import { StatsGraph } from "./statGraph";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";

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

const DataHeaderCaption: React.FC<{
  children: React.ReactNode;
  important?: boolean;
}> = (props) => (
  <Typography
    sx={{
      display: "block",
      lineHeight: theme.typography.body1.fontSize,
      color: props.important
        ? theme.palette.info.dark
        : theme.palette.primary.light,
    }}
    variant={props.important ? "body2" : "caption"}
  >
    {props.children}
  </Typography>
);

const HeaderCell: React.FC<{
  name: string;
  notNullNum: string;
  dType: string;
  columnData: ColumnStats;
  right?: boolean;
  type: CategoryMark;
}> = ({ name, notNullNum, dType, columnData, right, type }) => (
  <Box
    sx={{
      padding: theme.spacing(1),
      overflow: "visible",
      textAlign: right ? "right" : "left",
      cursor: "pointer",
      "&:hover": { background: theme.palette.info.light },
    }}
  >
    <Box sx={{ mb: theme.spacing(1) }}>
      {name}
      <OpenInFullIcon
        sx={{
          ml: theme.spacing(1),
          fontSize: theme.typography.caption.fontSize,
        }}
      />
    </Box>
    <DataHeaderCaption important>Type: {type}</DataHeaderCaption>
    <DataHeaderCaption>Not Null: {notNullNum}</DataHeaderCaption>
    <DataHeaderCaption>DataType: {dType}</DataHeaderCaption>
    <Box>
      <StatsGraph isSimple {...columnData} />
    </Box>
  </Box>
);

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

  const showFullSizeColumnInfo = useCallback(() => {}, []);

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

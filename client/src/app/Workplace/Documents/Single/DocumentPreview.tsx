import { TableFix } from "app/Workplace/common/Table";
import {
  useColumnsStatsDocumentQuery,
  useDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import React, { useMemo, useState } from "react";
import { zipObject, unzip, values, keys, first } from "lodash";
import {
  CategoricalData,
  CategoryMark,
  ColumnStats,
  DocumentStatsInfo,
  NumericData,
} from "ducks/reducers/types";
import { BallTriangle } from "react-loader-spinner";
import { theme } from "globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";
import { Box, Pagination, Paper, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";
import { Fixed } from "app/Workplace/common/Table/types";

const convertData = (data: Record<string, string | number>) =>
  unzip(values(data).map((x) => values(x as any))).map((zipArr) =>
    zipObject(keys(data), zipArr)
  );

enum PandasInfoColumns {
  columnName = "column_name",
  dataType = "data_type",
  nonNullCount = "non_null_count",
}
const findFieldInInfo = (
  info: DocumentStatsInfo,
  field: PandasInfoColumns,
  column: string
) => {
  const columnInx = info.column_name.findIndex((x) => x === column);

  return info[field][columnInx];
};

const DataHeaderCaption: React.FC<{ children: React.ReactNode }> = (props) => (
  <Box>
    <Typography sx={{ color: theme.palette.primary.light }} variant="caption">
      {props.children}
    </Typography>
  </Box>
);

const HeaderCell: React.FC<{
  name: string;
  notNullNum: string;
  dType: string;
  columnData: ColumnStats;
  right?: boolean;
}> = ({ name, notNullNum, dType, columnData, right }) => (
  <Box sx={{ overflow: "visible", textAlign: right ? "right" : "left" }}>
    <Box>{name}</Box>
    <DataHeaderCaption>Not Null: {notNullNum}</DataHeaderCaption>
    <DataHeaderCaption>Type: {dType}</DataHeaderCaption>
    <Box>
      <StatsGraph isSimple {...columnData} />
    </Box>
  </Box>
);

const CustomTooltip: React.FC<any> = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = first(payload) as any;
    return (
      <Paper
        sx={{
          p: theme.spacing(1),
        }}
      >
        <Typography sx={{ color: data.fill }}>
          {data.payload.longName}: {data.value}
        </Typography>
      </Paper>
    );
  }

  return null;
};

const convertDataForBarNumeric = (data: NumericData[]) =>
  data.map((x) => ({
    ...x,
    longName: `(${x.left},${x.right})`,
    name: (x.left + x.right) / 2,
  }));

const convertDataForBarCategoric = (data: CategoricalData[]) =>
  data.map((x) => ({
    ...x,
    longName: x.name,
  }));

const StatsGraph: React.FC<ColumnStats & { isSimple?: boolean }> = ({
  type,
  data,
  isSimple,
}) => (
  <Box>
    <BarChart
      width={120}
      height={100}
      margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
      data={
        type === CategoryMark.numeric
          ? convertDataForBarNumeric(data as NumericData[])
          : type === CategoryMark.categorical
          ? convertDataForBarCategoric(data as CategoricalData[])
          : []
      }
    >
      {!isSimple && (
        <>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
        </>
      )}

      <Tooltip
        wrapperStyle={{ zIndex: theme.zIndex.tooltip }}
        position={{ x: -30, y: 100 }}
        content={CustomTooltip}
      />

      <Bar dataKey="value" fill={theme.palette.info.main} />
    </BarChart>
  </Box>
);

export const DocumentPreview: React.FC<{ docName: string }> = ({ docName }) => {
  const [page, setPage] = useState<number>(1);
  const { data, isLoading } = useDocumentQuery({ filename: docName, page });
  const { data: infoData } = useInfoStatsDocumentQuery(docName);
  const { data: columnsStats } = useColumnsStatsDocumentQuery(docName);

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

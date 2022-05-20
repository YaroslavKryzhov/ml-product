import { Box, Divider, Typography } from "@mui/material";
import { TableFix } from "app/Workplace/common/Table";
import { InfoChip } from "components/infoChip";
import { count } from "console";
import {
  useColumnMarksDocumentQuery,
  useDescribeDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import { entries, fill, first, zip } from "lodash";
import moment from "moment";
import { compose, map, zipObj, values, keys } from "ramda";
import React, { useMemo } from "react";

enum DescribeRows {
  propNames = " ",
  firstQuantile = "25%",
  secondQuantile = "50%",
  thirdQuantile = "75%",
  count = "count",
  max = "max",
  mean = "mean",
  min = "min",
  std = "std",
}

// entries(
//   zipObj(
//     composeAny(keys, first, values)(describeData),
//     zip(...composeAny(map(values), values)(describeData))
//   )
// ).map(([key, values]) =>
//   zipObj(
//     [DescribeRows.propNames, ...keys(describeData)],
//     [key, ...values]
//   )
// )

const composeAny = compose as any;

export const MainInfo: React.FC<{ docName: string }> = ({ docName }) => {
  const { data: describeData } = useDescribeDocumentQuery(docName);
  const { data: infoData } = useInfoStatsDocumentQuery(docName);

  // const { data: columnMarks } = useColumnMarksDocumentQuery(docName);

  // const isNumeric = (name: string) => columnMarks?.numeric.includes(name);
  // const isCategorial = (name: string) =>
  //   columnMarks?.categorical.includes(name);

  const describeColumns = useMemo(
    () =>
      describeData
        ? [DescribeRows.propNames, ...keys(describeData)].map((x) => ({
            accessor: String(x),
            Header: x,
            width: DescribeRows.propNames === x ? 80 : undefined,
          }))
        : [],
    [describeData]
  );

  const describeDataRows = useMemo(
    () =>
      describeData
        ? entries(
            zipObj(
              composeAny(keys, first, values)(describeData),
              zip(...composeAny(map(values), values)(describeData))
            )
          ).map(([key, values]) =>
            zipObj(
              [DescribeRows.propNames, ...(keys(describeData) as string[])],
              [key, ...values]
            )
          )
        : [],
    [describeData]
  );

  const infoColumns = useMemo(
    () =>
      infoData
        ? keys(infoData).map((x) => ({
            accessor: String(x),
            Header: x,
          }))
        : [],
    [infoData]
  );

  const infoDataRows = useMemo(
    () =>
      infoData
        ? zip(...values(infoData).map(values)).map((x) =>
            zipObj(keys(infoData), x)
          )
        : [],
    [infoData]
  );

  console.log(infoData, infoDataRows);

  // if (!describeColumns.length) return null;

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Основное
      </Typography>
      <Box>
        <Typography variant="body1">Pandas Description</Typography>
        <TableFix
          isFirstColumnFixed
          columns={describeColumns}
          data={describeDataRows}
        />

        <Typography sx={{ mt: theme.spacing(3) }} variant="body1">
          Pandas Info
        </Typography>
      </Box>

      <TableFix columns={infoColumns} data={infoDataRows} />
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

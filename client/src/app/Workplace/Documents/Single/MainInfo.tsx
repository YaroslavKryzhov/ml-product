import { Box, Divider, Skeleton, Typography } from "@mui/material";
import { TableFix } from "components/Table";
import { useDescribeDocumentQuery } from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import { entries, first, zip } from "lodash";
import { compose, map, zipObj, values, keys } from "ramda";
import React, { useMemo } from "react";
import { useParams } from "react-router-dom";
import { DocumentPreview } from "./DocumentPreview";

enum DescribeRows {
  propNames = "Name",
  firstQuantile = "first_percentile",
  secondQuantile = "second_percentile",
  thirdQuantile = "third_percentile",
  count = "count",
  max = "max",
  mean = "mean",
  min = "min",
  std = "std",
}

const composeAny = compose as any;

export const MainInfo: React.FC = () => {
  const { docName } = useParams();
  const { data: describeData, isFetching: describeLoading } =
    useDescribeDocumentQuery(docName!);

  const describeColumns = useMemo(
    () =>
      describeData
        ? values(DescribeRows).map((x) => ({
            accessor: String(x),
            Header: x,
            width: DescribeRows.propNames === x ? 120 : undefined,
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

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(3) }} variant="h5">
        Основное
      </Typography>
      <Box>
        <DocumentPreview />
        <Typography sx={{ mt: theme.spacing(3) }} variant="body1">
          Pandas Description
        </Typography>
        {describeLoading ? (
          <Skeleton variant="rectangular" width="100%" height={300} />
        ) : (
          <TableFix
            compact
            isFirstColumnFixed
            columns={describeColumns}
            data={describeDataRows}
          />
        )}
      </Box>

      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

import { TableFix } from "app/Workplace/common/Table";
import {
  useDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import React, { useMemo, useState } from "react";
import { zipObject, unzip, values, keys } from "lodash";
import { theme } from "globalStyle/theme";
import { Box, Pagination, Skeleton } from "@mui/material";
import { Fixed } from "app/Workplace/common/Table/types";
import { HeaderCell } from "./HeaderCell";
import { useParams } from "react-router-dom";

const convertData = (data: Record<string, string | number>) =>
  unzip(values(data).map((x) => values(x as any))).map((zipArr) =>
    zipObject(keys(data), zipArr)
  );

export const DocumentPreview: React.FC = () => {
  const { docName } = useParams();
  const [page, setPage] = useState<number>(1);
  const { data, isFetching: isDocLoading } = useDocumentQuery({
    filename: docName!,
    page,
  });
  const { data: infoData, isFetching: isInfoLoading } =
    useInfoStatsDocumentQuery(docName!);

  const convertedData = useMemo(
    () => (data?.records ? convertData(data.records) : []),
    [data]
  );

  const columns = useMemo(
    () =>
      infoData
        ? infoData.map((df, inx, arr) => ({
            accessor: df.name,
            fixed: inx === arr.length - 1 ? Fixed.right : Fixed.left,
            Header: <HeaderCell {...df} right={inx === arr.length - 1} />,
          }))
        : [],
    [infoData]
  );

  return (
    <Box>
      {isDocLoading || isInfoLoading ? (
        <Skeleton variant="rectangular" width="100%" height={500} />
      ) : (
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
      )}
      {isInfoLoading ? (
        <Skeleton
          sx={{ mt: theme.spacing(2) }}
          variant="rectangular"
          width={300}
          height={32}
        />
      ) : (
        <Pagination
          sx={{ mt: theme.spacing(2) }}
          page={page}
          onChange={(_, page) => setPage(page)}
          count={data?.total}
          variant="outlined"
          shape="rounded"
        />
      )}
    </Box>
  );
};

import { TableFix } from "components/Table";
import {
  useDocumentQuery,
  useInfoStatsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import React, { useContext, useState } from "react";
import { zipObject, unzip, values, keys } from "lodash";
import { theme } from "globalStyle/theme";
import { Box, IconButton, Pagination, Skeleton } from "@mui/material";
import { Fixed } from "components/Table/types";
import { HeaderCell } from "./HeaderCell";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import { useDispatch } from "react-redux";
import { setDialog } from "ducks/reducers/dialog";
import { T } from "ramda";
import { HeightContext } from "components/Dialog";

const convertData = (data: Record<string, (string | number)[]>) =>
  unzip(values(data).map((x) => values(x as any))).map((zipArr) =>
    zipObject(keys(data), zipArr)
  );

export const DocumentPreview: React.FC<{
  docId: string;
  isInnerOpened?: boolean;
}> = ({ docId, isInnerOpened }) => {
  const dispatch = useDispatch();
  const [page, setPage] = useState<number>(1);
  const { data, isFetching: isDocLoading } = useDocumentQuery({
    dataframe_id: docId,
    page,
  });
  const { data: infoData, isFetching: isInfoLoading } =
    useInfoStatsDocumentQuery(docId);

  const convertedData = data?.records ? convertData(data.records) : [];

  const columns = infoData
    ? infoData.map((df, inx, arr) => ({
        accessor: df.name,
        fixed: inx === arr.length - 1 ? Fixed.right : Fixed.left,
        Header: <HeaderCell {...df} right={inx === arr.length - 1} />,
      }))
    : [];

  const openFulScreen = () =>
    dispatch(
      setDialog({
        title: `Данные`,
        Content: <DocumentPreview docId={docId} isInnerOpened />,
        onDismiss: T,
        dismissText: "Закрыть",
        fullWidth: true,
        fullHeight: true,
      })
    );

  const fullScreenTableHeight = useContext(HeightContext);

  return (
    <Box>
      {isDocLoading || isInfoLoading ? (
        <Skeleton variant="rectangular" width="100%" height={500} />
      ) : (
        <Box sx={{ position: "relative", width: "100%" }}>
          <TableFix
            compact
            offHeaderPaddings
            defaultColumnSizing={{ minWidth: 135 }}
            forceResize
            resizable
            data={convertedData}
            columns={columns}
            tableMaxHeight={`${
              isInnerOpened ? fullScreenTableHeight - 50 : 500
            }px`}
          />
          {!isInnerOpened && (
            <Box sx={{ position: "absolute", right: 5, bottom: 5 }}>
              <IconButton
                sx={{
                  backgroundColor: theme.palette.info.light,
                  color: theme.palette.info.main,
                  fontSize: "30px",
                  borderRadius: theme.shape.borderRadius,
                  opacity: "0.6",
                  "&:hover": {
                    backgroundColor: theme.palette.info.dark,
                    color: theme.palette.info.light,
                    opacity: "1",
                  },
                }}
                onClick={openFulScreen}
              >
                <OpenInNewIcon fontSize="inherit" />
              </IconButton>
            </Box>
          )}
        </Box>
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

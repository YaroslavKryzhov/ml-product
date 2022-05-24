import React, { useCallback, useMemo } from "react";
import {
  CategoricalData,
  CategoryMark,
  ColumnStats,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { Box, Grid, Typography } from "@mui/material";
import { StatsGraph } from "./statGraph";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useAppDispatch } from "ducks/hooks";
import { keys, T } from "ramda";
import { setDialog } from "ducks/reducers/dialog";
import { TableFix } from "app/Workplace/common/Table";
import { useDescribeDocumentQuery } from "ducks/reducers/api/documents.api";
import { useDocumentNameForce } from "../../hooks";
import { INFO_WIDTH } from "./contants";

type HeaderCellType = {
  name: string;
  notNullNum: string;
  dType: string;
  columnData: ColumnStats;
  right?: boolean;
  type: CategoryMark;
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

const MoreColumnInfo: React.FC<Omit<HeaderCellType, "right">> = ({
  name,
  notNullNum,
  dType,
  columnData,
  type,
}) => {
  const docName = useDocumentNameForce();
  const { data: describeData } = useDescribeDocumentQuery(docName!);
  const describeDataMerged = useMemo(
    () =>
      describeData ? { type, notNullNum, dType, ...describeData[name] } : {},
    [notNullNum, dType, type, describeData, name]
  );

  const describeColumns = useMemo(
    () =>
      describeDataMerged
        ? keys(describeDataMerged).map((x, _, arr) => ({
            Header: String(x),
            accessor: String(x),
            maxWidth: 150,
            width: INFO_WIDTH / arr.length,
          }))
        : [],
    [describeDataMerged]
  );

  return (
    <Box>
      <StatsGraph {...columnData} />
      <Box
        sx={{
          mt: theme.spacing(2),
          background: theme.palette.secondary.light,
          borderRadius: theme.shape.borderRadius,
        }}
      >
        {type === CategoryMark.categorical && (
          <Grid
            container
            sx={{
              justifyContent: "center",
            }}
          >
            {(columnData.data as CategoricalData[]).map((x) => (
              <Grid
                item
                sx={{ padding: `${theme.spacing(2)} ${theme.spacing(4)}` }}
              >
                <Typography variant="body2">
                  {x.name}: {x.value.toFixed(2)}
                </Typography>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      <Box sx={{ mt: theme.spacing(4) }}>
        <TableFix columns={describeColumns} data={[describeDataMerged]} />
      </Box>
    </Box>
  );
};

export const HeaderCell: React.FC<HeaderCellType> = (props) => {
  const dispatch = useAppDispatch();
  const setDialogProps = useCallback(() => {
    dispatch(
      setDialog({
        title: `Подробности о ${props.name}`,
        Content: <MoreColumnInfo {...props} />,
        onDismiss: T,
        dismissText: "Закрыть",
      })
    );
  }, []);

  return (
    <Box
      onClick={setDialogProps}
      sx={{
        flexGrow: 1,
        padding: theme.spacing(1),
        overflow: "visible",
        textAlign: props.right ? "right" : "left",
        cursor: "pointer",
        "&:hover": { background: theme.palette.info.light },
      }}
    >
      <Box sx={{ mb: theme.spacing(1) }}>
        {props.name}
        <OpenInFullIcon
          sx={{
            ml: theme.spacing(1),
            fontSize: theme.typography.caption.fontSize,
          }}
        />
      </Box>
      <DataHeaderCaption important>
        Type: {props.type || "NO TYPE"}
      </DataHeaderCaption>
      <DataHeaderCaption>Not Null: {props.notNullNum}</DataHeaderCaption>
      <DataHeaderCaption>DataType: {props.dType}</DataHeaderCaption>
      {props.columnData && (
        <Box
          sx={{
            display: "flex",
            justifyContent: props.right ? "flex-end" : "flex-start",
          }}
        >
          <StatsGraph isSimple {...props.columnData} />
        </Box>
      )}
    </Box>
  );
};

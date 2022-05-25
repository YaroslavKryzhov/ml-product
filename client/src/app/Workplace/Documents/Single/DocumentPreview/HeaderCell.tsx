import React, { useCallback, useMemo } from "react";
import {
  CategoricalData,
  CategoryMark,
  ColumnStats,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { Box, Tooltip, Typography } from "@mui/material";
import { StatsGraph } from "./statGraph";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useAppDispatch } from "ducks/hooks";
import { keys, T } from "ramda";
import { setDialog } from "ducks/reducers/dialog";
import { TableFix } from "app/Workplace/common/Table";
import { useDescribeDocumentQuery } from "ducks/reducers/api/documents.api";
import { useDocumentNameForce } from "../../hooks";
import { INFO_WIDTH } from "./contants";
import { CellProps } from "react-table";
import { OverflowText } from "app/Workplace/common/styles";

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

  const CellUnit: React.FC<{ value: string }> = ({ value }) => (
    <Tooltip followCursor title={value}>
      <Box
        sx={{
          padding: `${theme.spacing(1)} ${theme.spacing(1)}`,
          ...OverflowText,
        }}
      >
        {String(value)}
      </Box>
    </Tooltip>
  );

  const describeColumns = useMemo(
    () =>
      describeDataMerged
        ? keys(describeDataMerged).map((x, _, arr) => ({
            Header: <CellUnit value={x} />,
            Cell: (x: CellProps<{}>) => <CellUnit value={x.cell.value} />,
            accessor: String(x),
            maxWidth: 150,
            width: INFO_WIDTH / arr.length,
          }))
        : [],
    [describeDataMerged]
  );

  return (
    <Box
      sx={{ display: "flex", alignItems: "center", flexDirection: "column" }}
    >
      <StatsGraph {...columnData} />
      <Box
        sx={{
          mt: theme.spacing(2),
          background: theme.palette.secondary.light,
          borderRadius: theme.shape.borderRadius,
        }}
      >
        {type === CategoryMark.categorical && (
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(3,1fr)",
              padding: `${theme.spacing(2)} ${theme.spacing(4)}`,
              gap: `${theme.spacing(1)} ${theme.spacing(4)}`,
            }}
          >
            {(columnData.data as CategoricalData[]).map((x) => (
              <Box
                sx={{
                  display: "flex",
                  overflow: "hidden",
                  justifyContent: "space-between",
                  gap: theme.spacing(2),
                }}
              >
                <Tooltip followCursor title={x.name}>
                  <Typography
                    sx={{
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                    }}
                    variant="body2"
                  >
                    {x.name}:
                  </Typography>
                </Tooltip>

                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  {x.value.toFixed(2)}
                </Typography>
              </Box>
            ))}
          </Box>
        )}
      </Box>

      <Box sx={{ mt: theme.spacing(4) }}>
        <TableFix
          offHeaderPaddings
          offCellsPaddings
          columns={describeColumns}
          data={[describeDataMerged]}
        />
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
        overflow: "hidden",
        textAlign: props.right ? "right" : "left",
        cursor: "pointer",
        "&:hover": { background: theme.palette.info.light },
      }}
    >
      <Box sx={{ mb: theme.spacing(1), display: "flex", ...OverflowText }}>
        <Tooltip followCursor title={props.name}>
          <Box sx={{ ...OverflowText }}>{props.name}</Box>
        </Tooltip>

        <OpenInFullIcon
          sx={{
            ml: theme.spacing(1),
            mt: "7px",
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

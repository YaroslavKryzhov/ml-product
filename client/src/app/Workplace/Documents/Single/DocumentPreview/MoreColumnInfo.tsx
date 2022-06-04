import React, { useMemo } from "react";
import { CategoricalData, CategoryMark, DFInfo } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { Box, Tooltip, Typography } from "@mui/material";
import { StatsGraph } from "./statGraph";
import { isNil, keys } from "ramda";
import { TableFix } from "app/Workplace/common/Table";
import { useDescribeDocumentQuery } from "ducks/reducers/api/documents.api";
import { useDocumentNameForce } from "../../hooks";
import { INFO_WIDTH } from "./contants";
import { CellProps } from "react-table";
import { OverflowText } from "app/Workplace/common/styles";
import { entries } from "lodash";

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

export const MoreColumnInfo: React.FC<DFInfo> = ({
  type,
  data,
  name,
  not_null_count,
  data_type,
}) => {
  const docName = useDocumentNameForce();
  const { data: describeData } = useDescribeDocumentQuery(docName!);
  const describeDataMerged = useMemo(
    () =>
      describeData
        ? {
            type,
            not_null_count,
            data_type,
            ...Object.fromEntries(
              entries(describeData)
                .filter(([_, value]) => !isNil(value[name]))
                .map(([key, value]) => [key, value[name]])
            ),
          }
        : {},
    [not_null_count, data_type, type, describeData, name]
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
      <StatsGraph data={data} type={type} />
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
            {(data as CategoricalData[]).map((x) => (
              <Box
                key={x.name}
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

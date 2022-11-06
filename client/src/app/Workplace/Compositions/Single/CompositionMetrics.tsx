import { Box, Divider, Typography } from "@mui/material";
import { CellUnit } from "app/Workplace/Documents/Single/DocumentPreview/MoreColumnInfo";
import { TableFix } from "components/Table";
import { useCompositionInfoQuery } from "ducks/reducers/api/compositions.api";
import { theme } from "globalStyle/theme";
import { keys } from "lodash";
import { isEmpty, isNil } from "ramda";
import React from "react";
import { CellProps } from "react-table";
import {
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Label,
  Scatter,
  ScatterChart,
} from "recharts";

export const CompositionMetrics: React.FC<{ model_name: string }> = ({
  model_name,
}) => {
  const { data: modelData } = useCompositionInfoQuery({
    model_name,
  });

  const describeDataMerged = modelData
    ? Object.fromEntries(
        Object.entries(modelData.report.metrics).filter(
          ([key, val]) =>
            !isNil(val) &&
            ![
              "fpr",
              "tpr",
              "tpr_macro",
              "fpr_macro",
              "tpr_micro",
              "fpr_micro",
            ].includes(key)
        )
      )
    : {};

  const describeColumns = describeDataMerged
    ? keys(describeDataMerged).map((x, _, arr) => ({
        Header: <CellUnit value={x} />,
        Cell: (x: CellProps<{}>) => <CellUnit value={x.cell.value} />,
        accessor: String(x),
        maxWidth: 150,
      }))
    : [];

  const chartData =
    modelData &&
    !isEmpty(modelData.report.metrics.fpr) &&
    modelData.report.metrics.fpr?.map((fprVal, inx, arr) => ({
      fpr: fprVal,
      tpr: modelData.report.metrics.tpr![inx],
    }));

  const chartDataMacro =
    modelData &&
    !isEmpty(modelData.report.metrics.fpr_macro) &&
    modelData.report.metrics.fpr_macro?.map((fprVal, inx, arr) => ({
      fpr_macro: fprVal,
      tpr_macro: modelData.report.metrics.tpr_macro![inx],
    }));

  const chartDataMicro =
    modelData &&
    !isEmpty(modelData.report.metrics.fpr_micro) &&
    modelData.report.metrics.fpr_micro?.map((fprVal, inx, arr) => ({
      fpr_micro: fprVal,
      tpr_micro: modelData.report.metrics.tpr_micro![inx],
    }));

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(3) }} variant="h5">
        Метрики
      </Typography>
      <Box
        sx={{
          display: "flex",
          gap: theme.spacing(1),
          flexWrap: "wrap",
        }}
      >
        {!isEmpty(describeDataMerged) && (
          <TableFix
            offHeaderPaddings
            offCellsPaddings
            columns={describeColumns}
            data={[describeDataMerged]}
          />
        )}
      </Box>
      <Box
        sx={{
          mt: theme.spacing(5),
        }}
      >
        {chartData && (
          <ScatterChart
            width={1000}
            height={800}
            margin={{ bottom: 20, top: 10, right: 10, left: 10 }}
          >
            <CartesianGrid />
            <XAxis dataKey="fpr" type="number">
              <Label value="FPR" offset={-15} position="insideBottom" />
            </XAxis>

            <YAxis type="number" dataKey="tpr">
              <Label
                value="TPR"
                position="insideLeft"
                angle={-90}
                offset={10}
              />
            </YAxis>
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={chartData} fill={theme.palette.info.main} line />
          </ScatterChart>
        )}
        {chartDataMacro && (
          <ScatterChart
            width={1000}
            height={800}
            margin={{ bottom: 20, top: 10, right: 10, left: 10 }}
          >
            <CartesianGrid />
            <XAxis dataKey="fpr_macro" type="number">
              <Label value="FPR MACRO" offset={-15} position="insideBottom" />
            </XAxis>

            <YAxis type="number" dataKey="tpr_macro">
              <Label
                value="TPR MACRO"
                position="insideLeft"
                angle={-90}
                offset={10}
              />
            </YAxis>
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter
              data={chartDataMacro}
              fill={theme.palette.info.main}
              line
            />
          </ScatterChart>
        )}

        {chartDataMicro && (
          <ScatterChart
            width={1000}
            height={800}
            margin={{ bottom: 20, top: 10, right: 10, left: 10 }}
          >
            <CartesianGrid />
            <XAxis dataKey="fpr_micro" type="number">
              <Label value="FPR MICRO" offset={-15} position="insideBottom" />
            </XAxis>

            <YAxis type="number" dataKey="tpr_micro">
              <Label
                value="TPR MICRO"
                position="insideLeft"
                angle={-90}
                offset={10}
              />
            </YAxis>
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter
              data={chartDataMicro}
              fill={theme.palette.info.main}
              line
            />
          </ScatterChart>
        )}
      </Box>
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(2) }} />
    </Box>
  );
};

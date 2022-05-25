import React from "react";
import { first } from "lodash";
import {
  CategoricalData,
  CategoryMark,
  ColumnStats,
  NumericData,
} from "ducks/reducers/types";
import { theme, withOpacity } from "globalStyle/theme";
import { Box, Paper, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";
import { INFO_WIDTH } from "./contants";

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
    name: ((x.left + x.right) / 2).toFixed(3),
  }));

const convertDataForBarCategoric = (data: CategoricalData[]) =>
  data.map((x) => ({
    ...x,
    longName: x.name,
  }));

export const StatsGraph: React.FC<ColumnStats & { isSimple?: boolean }> = ({
  type,
  data,
  isSimple,
}) => (
  <Box>
    <BarChart
      width={isSimple ? 120 : INFO_WIDTH}
      height={isSimple ? 100 : 370}
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
          <YAxis
            tickFormatter={(n: number) => {
              const num = n.toPrecision(2);

              return String(
                String(num).length > 5 ? Number(num).toExponential() : num
              );
            }}
          />
        </>
      )}

      <Tooltip
        wrapperStyle={{ zIndex: theme.zIndex.tooltip }}
        position={isSimple ? { x: -30, y: 100 } : undefined}
        content={CustomTooltip}
        cursor={{ fill: withOpacity(theme.palette.info.main, 0.3) }}
      />

      <Bar dataKey="value" fill={theme.palette.info.main} />
    </BarChart>
  </Box>
);

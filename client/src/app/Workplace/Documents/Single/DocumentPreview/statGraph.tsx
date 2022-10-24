import React, { useEffect, useRef, useState } from "react";
import { first } from "lodash";
import {
  CategoricalData,
  CategoryMark,
  NumericData,
} from "ducks/reducers/types";
import { theme, withOpacity } from "globalStyle/theme";
import { Box, Paper, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";
import { INFO_WIDTH, SIMPLE_HEIGHT } from "./contants";

const CustomTooltip: React.FC<any> = ({ active, payload, ...rest }) => {
  if (active && payload && payload.length) {
    const data = first(payload) as any;

    return (
      <Box>
        <Paper
          sx={{
            p: theme.spacing(1),
            zIndex: theme.zIndex.tooltip,
          }}
        >
          <Typography sx={{ color: data.fill }}>
            {data.payload.longName}: {data.payload.displayValue || data.value}
          </Typography>
        </Paper>
      </Box>
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
    displayValue: (x.value * 100).toFixed(2) + "%",
  }));

export const StatsGraph: React.FC<{
  type: CategoryMark;
  data: (NumericData | CategoricalData)[];
  isSimple?: boolean;
}> = ({ type, data, isSimple }) => {
  const [boxPosition, setBoxPosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });

  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isSimple) return;
    const handler = () => {
      if (!ref.current) return;
      const rect = ref.current.getBoundingClientRect();

      setBoxPosition({ x: rect.left, y: rect.top });
    };

    const container = ref.current;

    container?.addEventListener("mousemove", handler);

    handler();

    return () => container?.removeEventListener("mousemove", handler);
  }, [isSimple]);

  return (
    <Box ref={ref}>
      <BarChart
        width={isSimple ? 117 : INFO_WIDTH}
        height={isSimple ? SIMPLE_HEIGHT : 370}
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
          allowEscapeViewBox={{ x: true, y: true }}
          wrapperStyle={{
            zIndex: theme.zIndex.tooltip,
            position: isSimple ? "fixed" : "absolute",
            left: boxPosition.x,
            top: boxPosition.y,
          }}
          content={CustomTooltip}
          cursor={{ fill: withOpacity(theme.palette.info.main, 0.3) }}
        />

        <Bar dataKey="value" fill={theme.palette.info.main} />
      </BarChart>
    </Box>
  );
};

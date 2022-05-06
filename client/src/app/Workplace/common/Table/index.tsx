import React, { useLayoutEffect, useRef, useState } from "react";
import {
  useColumnOrder,
  useFlexLayout,
  useResizeColumns,
  useSortBy,
  useTable,
  Hooks,
  usePagination,
  Row,
} from "react-table";
import { StyledTable } from "./styled";
import TableFixBody from "./components/Body";
import TableFixHeader from "./components/Header";
import { DEFAULT_COLUMN } from "./const";
import { TableFixProps } from "./types";
import { Paper } from "@mui/material";
import moment from "moment";
export * as TableFixTypes from "./types";

export const compareDate = (field: string) => (a: Row, b: Row) =>
  moment(a.values[field]).utc() > moment(b.values[field]).utc() ? 1 : -1;

const View: React.FC<TableFixProps> = (props) => {
  const [colsWithWidth, setColsWithWidth] = useState(props.columns);
  const containerRef = useRef<HTMLTableElement | null>(null);

  const hooks: (<D extends object = {}>(hooks: Hooks<D>) => void)[] = [
    useFlexLayout,
    useColumnOrder,
    useSortBy,
    usePagination,
    useResizeColumns,
  ];

  const { getTableProps, getTableBodyProps, headerGroups, prepareRow, page } =
    useTable(
      {
        columns: colsWithWidth,
        data: props.data,
        defaultColumn: DEFAULT_COLUMN,
        initialState: {
          pageSize: props.data.length || 50,
          pageIndex: 0,
          columnOrder: props.columnOrder || [],
          sortBy: props.sortBy || [],
        },
      },
      ...hooks
    );

  useLayoutEffect(() => {
    const handler = () => {
      if (containerRef.current) {
        const calcHeaders: any[] = headerGroups.length
          ? headerGroups[0].headers
          : props.columns;
        const sumWidth = calcHeaders.reduce(
          (acc, c) => acc + (Number(c.width) || DEFAULT_COLUMN.width),
          0
        );

        const contW = containerRef.current.getBoundingClientRect().width;

        const newColumns = calcHeaders.map((c) => ({
          ...c,
          width: (contW * (Number(c.width) || DEFAULT_COLUMN.width)) / sumWidth,
        }));
        setColsWithWidth(newColumns);
      }
    };
    handler();

    window.addEventListener("resize", handler);

    return () => window.addEventListener("resize", handler);
  }, [props.columns.toString(), props.forceResize]);

  return (
    <Paper elevation={3} ref={containerRef}>
      <StyledTable
        {...getTableProps()}
        maxHeight={props.tableMaxHeight}
        isFirstColumnFixed={props.isFirstColumnFixed}
      >
        <TableFixHeader
          // TODO
          // resizable={props.resizable}
          headerGroups={headerGroups}
        />
        <TableFixBody
          rowActions={props.rowActions}
          rowHoverable={props.rowHoverable}
          page={page}
          prepareRow={prepareRow}
          tableBodyProps={getTableBodyProps()}
        />
      </StyledTable>
    </Paper>
  );
};

const TableFix = React.memo(View);

export { TableFix };

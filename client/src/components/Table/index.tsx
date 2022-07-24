import React, {
  useContext,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
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
import { Box, Paper } from "@mui/material";
import moment from "moment";
import { MenuContext } from "app/Workplace";
import { theme } from "globalStyle/theme";
import { nanoid } from "@reduxjs/toolkit";
import { isEmpty } from "lodash";
export * as TableFixTypes from "./types";

export const compareDate = (field: string) => (a: Row, b: Row) =>
  moment(a.values[field]).utc() > moment(b.values[field]).utc() ? 1 : -1;

const View: React.FC<TableFixProps> = (props) => {
  const [colsWithWidth, setColsWithWidth] = useState(props.columns);
  const containerRef = useRef<HTMLTableElement | null>(null);
  const { menuOpened } = useContext(MenuContext);
  const [forceResize, setForceResize] = useState("");
  const firstRender = useRef(true);

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
        defaultColumn: {
          width: props.defaultColumnSizing?.width || DEFAULT_COLUMN.width,
          minWidth:
            props.defaultColumnSizing?.minWidth || DEFAULT_COLUMN.minWidth,
          maxWidth:
            props.defaultColumnSizing?.maxWidth || DEFAULT_COLUMN.maxWidth,
        },
        initialState: {
          pageSize: 50,
          pageIndex: 0,
          columnOrder: props.columnOrder || [],
          sortBy: props.sortBy || [],
        },
      },
      ...hooks
    );

  // untested
  useEffect(() => {
    setColsWithWidth(props.columns);
    setForceResize(nanoid());
  }, [props.columns]);

  //end

  useLayoutEffect(() => {
    // toDO throttle and sum chnges
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
    return () => window.removeEventListener("resize", handler);
  }, [forceResize, colsWithWidth.length]);

  useEffect(() => {
    if (!props.forceResize || firstRender.current) return;

    const interval = setInterval(() => setForceResize(nanoid()), 0);

    setTimeout(
      () => clearInterval(interval),
      theme.transitions.duration.complex
    );

    return () => clearInterval(interval);
  }, [menuOpened, props.forceResize]);

  useEffect(() => {
    firstRender.current = false;
  }, []);

  return (
    <Box
      ref={containerRef}
      sx={{
        display: "flex",
        justifyContent: "center",
        maxWidth: "100%",
      }}
    >
      <Paper
        elevation={3}
        sx={{ width: isEmpty(page) ? "100%" : "min-content", maxWidth: "100%" }}
      >
        <StyledTable
          {...getTableProps()}
          maxHeight={props.tableMaxHeight}
          isFirstColumnFixed={props.isFirstColumnFixed}
        >
          <TableFixHeader
            // TODO
            // resizable={props.resizable}
            headerGroups={headerGroups}
            offHeaderPaddings={props.offHeaderPaddings}
            compact={props.compact}
          />
          <TableFixBody
            offCellsPaddings={props.offCellsPaddings}
            compact={props.compact}
            rowActions={props.rowActions}
            rowHoverable={props.rowHoverable}
            page={page}
            prepareRow={prepareRow}
            tableBodyProps={getTableBodyProps()}
          />
        </StyledTable>
      </Paper>
    </Box>
  );
};

const TableFix = React.memo(View);

export { TableFix };

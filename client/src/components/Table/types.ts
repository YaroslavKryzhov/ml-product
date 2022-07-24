import React from "react";
import { Column, Row } from "react-table";

export enum Fixed {
  left = "left",
  right = "right",
  center = "center",
}

export type CustomColumn = Column & Partial<{ fixed: Fixed }>;

export type RowAction = {
  icon: React.ReactElement;
  name: string;
  onClick: (row: Row) => void;
};

export type TableFixProps = {
  compact?: boolean;
  offHeaderPaddings?: boolean;
  offCellsPaddings?: boolean;
  rowHoverable?: boolean;
  forceResize?: boolean;
  data: object[];
  columns: Column[];
  isFirstColumnFixed?: boolean;
  sortBy?: { id: string; desc: boolean }[]; // Add columnId and desc(bool), for set sorting by default
  defaultColumnSizing?: {
    minWidth?: number;
    width?: number;
    maxWidth?: number;
  };
  columnOrder?: string[]; // add id to column and place Array<ColumnId> here, to correct columns ordering
  tableMaxHeight?: string;
  resizable?: boolean;
  rowActions?: RowAction[];
  columnAlign?: string;
};

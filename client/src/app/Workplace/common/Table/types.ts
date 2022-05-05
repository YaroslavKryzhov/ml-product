import { Column } from "react-table";

export enum Fixed {
  left = "left",
  right = "right",
  center = "center",
}

export type CustomColumn = Column & Partial<{ fixed: Fixed }>;

export type TableFixProps = {
  forceResize?: any;
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
};

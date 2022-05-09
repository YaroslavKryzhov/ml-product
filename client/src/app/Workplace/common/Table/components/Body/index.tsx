import { SpeedDial, SpeedDialAction } from "@mui/material";
import { theme } from "globalStyle/theme";
import React from "react";
import { Row, TableBodyProps } from "react-table";
import { CustomColumn, RowAction } from "../../types";
import {
  StyledTableCell,
  StyledTableRow,
  EmptyData,
  TableFixContainer,
  CellValueContainer,
} from "./styled";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import { TABLE_PARTS } from "../../const";
import { useOverflow } from "app/Workplace/common/useOverflow";

type TableFixBodyProps = {
  page: Row<object>[];
  tableBodyProps: TableBodyProps;
  prepareRow: (row: Row<object>) => void;
  rowHoverable?: boolean;
  rowActions?: RowAction[];
};

export const ActionIconSx = {
  minHeight: 0,
  p: 0,
  m: 0,
  width: theme.typography.h6.fontSize,
  height: theme.typography.h6.fontSize,

  "&.MuiButtonBase-root": {
    ml: theme.spacing(1),
  },
};

const TableFixBody: React.FC<TableFixBodyProps> = ({
  page,
  tableBodyProps,
  prepareRow,
  rowHoverable,
  rowActions,
}) => (
  <TableFixContainer {...tableBodyProps}>
    {page?.length ? (
      page.map((row) => {
        prepareRow(row);
        const { key: rowKey, ...rowProps } = row.getRowProps();

        return (
          <StyledTableRow
            {...rowProps}
            key={rowKey}
            rowHoverable={rowHoverable}
          >
            {row.cells.map((cell, inx) => {
              const { key: cellKey, ...cellProps } = cell.getCellProps();

              return (
                <StyledTableCell
                  {...cellProps}
                  fixed={(cell.column as CustomColumn).fixed}
                  key={cellKey}
                >
                  <CellValueContainer>
                    {cell.render(TABLE_PARTS.Cell)}
                  </CellValueContainer>

                  {rowActions && !inx && (
                    <SpeedDial
                      className="speedDial"
                      ariaLabel="Row Actions"
                      FabProps={{
                        color: "secondary",
                      }}
                      sx={{
                        ml: theme.spacing(2),
                        "& button": ActionIconSx,
                        "& svg": {
                          width: theme.typography.body2.fontSize,
                          height: theme.typography.body2.fontSize,
                        },
                      }}
                      icon={
                        <MoreHorizIcon
                          sx={{ fontSize: theme.typography.body1.fontSize }}
                        />
                      }
                      direction="right"
                    >
                      {rowActions.map((action) => (
                        <SpeedDialAction
                          key={action.name}
                          icon={action.icon}
                          tooltipTitle={action.name}
                          onClick={() => action.onClick(row)}
                        />
                      ))}
                    </SpeedDial>
                  )}
                </StyledTableCell>
              );
            })}
          </StyledTableRow>
        );
      })
    ) : (
      <tr>
        <EmptyData>Данных не найдено</EmptyData>
      </tr>
    )}
  </TableFixContainer>
);

export default TableFixBody;

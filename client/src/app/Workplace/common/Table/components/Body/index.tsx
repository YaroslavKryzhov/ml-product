import React from "react";
import { Row, TableBodyProps } from "react-table";
import { TABLE_PARTS } from "../../const";
import { CustomColumn } from "../../types";
import {
  StyledTableCell,
  StyledTableRow,
  EmptyData,
  TableFixContainer,
} from "./styled";

type TableFixBodyProps = {
  page: Row<object>[];
  tableBodyProps: TableBodyProps;
  prepareRow: (row: Row<object>) => void;
};

const TableFixBody: React.FC<TableFixBodyProps> = ({
  page,
  tableBodyProps,
  prepareRow,
}) => (
  <TableFixContainer {...tableBodyProps}>
    {page?.length ? (
      page.map((row) => {
        prepareRow(row);
        const { key: rowKey, ...rowProps } = row.getRowProps();

        return (
          <StyledTableRow {...rowProps} key={rowKey}>
            {row.cells.map((cell) => {
              const { key: cellKey, ...cellProps } = cell.getCellProps();

              return (
                <StyledTableCell
                  {...cellProps}
                  fixed={(cell.column as CustomColumn).fixed}
                  key={cellKey}
                >
                  {cell.render(TABLE_PARTS.Cell)}
                </StyledTableCell>
              );
            })}
          </StyledTableRow>
        );
      })
    ) : (
      <EmptyData>Данных не найдено</EmptyData>
    )}
  </TableFixContainer>
);

export default TableFixBody;

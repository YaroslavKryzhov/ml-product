import React from "react";
import { HeaderGroup } from "react-table";
import { TABLE_PARTS } from "../../const";
import { CustomColumn } from "../../types";
import {
  HeadCellContent,
  SortedArrowUp,
  StyledHeadCell,
  StyledResizer,
  StyledTableHead,
} from "./styled";

type TableFixHeaderProps = {
  headerGroups: HeaderGroup<object>[];
  resizable?: boolean;
};

const TableFixHeader: React.FC<TableFixHeaderProps> = ({
  resizable,
  headerGroups,
}) => (
  <StyledTableHead>
    {headerGroups.map((headerGroup) => {
      const { key: groupKey, ...headerGroupProps } =
        headerGroup.getHeaderGroupProps();

      return (
        <tr {...headerGroupProps} key={groupKey}>
          {headerGroup.headers.map((column) => {
            const { key: headerKey, ...headerProps } = column.getHeaderProps();

            return (
              <StyledHeadCell
                fixed={(column as CustomColumn).fixed}
                {...headerProps}
                key={headerKey}
              >
                <HeadCellContent {...column.getSortByToggleProps()}>
                  {column.render(TABLE_PARTS.Header)}
                </HeadCellContent>
                {column.isSorted && (
                  <SortedArrowUp isFlipped={column.isSortedDesc} />
                )}
                {resizable && (
                  <StyledResizer
                    {...(resizable ? column.getResizerProps() : {})}
                  />
                )}
              </StyledHeadCell>
            );
          })}
        </tr>
      );
    })}
  </StyledTableHead>
);

export default TableFixHeader;

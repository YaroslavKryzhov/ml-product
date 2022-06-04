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
  offHeaderPaddings?: boolean;
  compact?: boolean;
};

const TableFixHeader: React.FC<TableFixHeaderProps> = ({
  resizable,
  headerGroups,
  offHeaderPaddings,
  compact,
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
                {...column.getSortByToggleProps()}
                fixed={(column as CustomColumn).fixed}
                {...headerProps}
                key={headerKey}
                offHeaderPaddings={offHeaderPaddings}
                compact={compact}
              >
                {typeof column.Header === "string" ? (
                  <HeadCellContent>
                    {column.render(TABLE_PARTS.Header)}
                  </HeadCellContent>
                ) : (
                  column.render(TABLE_PARTS.Header)
                )}

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

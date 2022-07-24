import React, { useRef, useEffect, useState } from "react";
import styled from "@emotion/styled";
import { Box, Tooltip } from "@mui/material";

const CellContainer = styled.div`
  overflow: hidden;
  display: block;
  text-overflow: ellipsis;
`;

const InvisibleCellContainer = styled.div`
  height: 0;
  visibility: hidden;
  display: table-caption;
`;

export const ElementWithTooltip: React.FC<{
  title: string;
  width: number;
  children: React.ReactNode;
}> = ({ title, width, children }) => {
  const elementRef = useRef<HTMLDivElement>(null);
  const [isVisibleTooltip, setIsVisibleTooltip] = useState<boolean>(false);

  useEffect(() => {
    if (elementRef.current) {
      const rect = elementRef.current.getBoundingClientRect();

      if (rect.width > width) {
        setIsVisibleTooltip(true);
      }
    }
  }, []);

  return (
    <>
      <InvisibleCellContainer ref={elementRef}>{title}</InvisibleCellContainer>

      <Tooltip followCursor title={isVisibleTooltip ? title : ""}>
        <CellContainer>{children}</CellContainer>
      </Tooltip>
    </>
  );
};

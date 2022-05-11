import styled from "@emotion/styled";
import { Box, Stack } from "@mui/material";
import { theme } from "globalStyle/theme";
import React, { useCallback, useEffect, useRef, useState } from "react";
import SwipeLeftIcon from "@mui/icons-material/SwipeLeft";

const HeapBox = styled.div<{ isHeap?: boolean }>`
  width: 300px;
  height: ${({ isHeap }) => (isHeap ? 240 : 120)}px;
  border: ${theme.additional.borderWidth}px solid ${theme.palette.primary.light};
  border-radius: ${theme.shape.borderRadiusRound}px;
  overflow: hidden;
`;

const HeapName = styled.div`
  background: ${theme.palette.primary.main};
  color: ${theme.palette.primary.contrastText};
  padding: ${theme.spacing(1)};
  font-size: ${theme.typography.body2.fontSize};
  text-align: center;
`;

const ItemWrapper = styled.div<{
  isDragging?: boolean;
  draggingRect?: DOMRect | null;
}>`
  border-radius: ${theme.shape.borderRadiusRound}px;
  padding: 0 ${theme.spacing(1)};
  display: flex;
  gap: ${theme.spacing(1)};
  background-color: ${theme.palette.primary.main};
  font-size: ${theme.typography.caption.fontSize};
  width: min-content;
  color: ${theme.palette.primary.contrastText};
  align-items: center;
  justify-content: space-between;
  position: relative;
  cursor: pointer;
  user-select: none;
  opacity: ${({ isDragging }) => (isDragging ? 0.3 : 1)};

  ${({ draggingRect }) =>
    draggingRect &&
    `
    position: absolute;
    left: ${draggingRect.left}px;
    top: ${draggingRect.top}px;
  `}

  &:hover {
    background-color: ${theme.palette.primary.light};
  }
`;

const HeapElements = styled.div`
  padding: ${theme.spacing(1)};
  display: fixed;
  gap: ${theme.spacing(1)};
  flex-wrap: wrap;
  width: 100%;
  justify-content: center;
  overflow-y: scroll;
`;

type CategoryItem = { value: string; label: string };

export type Distribution = {
  heap: string[];
  [key: string]: string[];
};

type CurrentDraging = {
  item: CategoryItem;
  startPosition: { x: number; y: number };
};

const Item: React.FC<
  CategoryItem & {
    onElementDragStart?: (val: CurrentDraging | null) => void;
    draggingRect?: DOMRect | null;
  }
> = (props) => {
  const ref = useRef<HTMLDivElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (isDragging) {
      const handler = () => {
        setIsDragging(false);
        props.onElementDragStart && props.onElementDragStart(null);
      };

      window.addEventListener("mouseup", handler);

      return () => window.removeEventListener("mouseup", handler);
    }
  }, [props.onElementDragStart, isDragging]);

  return (
    <ItemWrapper
      draggingRect={props.draggingRect}
      isDragging={isDragging}
      ref={ref}
      onMouseDown={(e: React.MouseEvent) => {
        setIsDragging(true);
        props.onElementDragStart &&
          props.onElementDragStart({
            item: { value: props.value, label: props.label },
            startPosition: { x: e.clientX, y: e.clientY },
          });
      }}
    >
      {props.label}
      <SwipeLeftIcon sx={{ fontSize: theme.typography.caption.fontSize }} />
    </ItemWrapper>
  );
};

const CategoryHeap: React.FC<
  CategoryItem & {
    items: string[];
    onElementDragStart: (val: CurrentDraging | null) => void;
  }
> = ({ value, label, items, onElementDragStart }) => {
  return (
    <HeapBox isHeap={value === "heap"}>
      <HeapName>{label}</HeapName>
      <HeapElements>
        {items.map((item) => (
          <Item
            key={item}
            onElementDragStart={onElementDragStart}
            label={item}
            value={item}
          />
        ))}
      </HeapElements>
    </HeapBox>
  );
};

export const Categorizer: React.FC<{
  categories: CategoryItem[];
  distribution: Distribution;
  distributionChange: (newDistribution: Distribution) => void;
  heap: { label: string; value: string };
}> = ({ categories, distribution, distributionChange, heap }) => {
  const [draggingEl, setDraggingEl] = useState<CurrentDraging | null>(null);
  const [draggingRect, setDraggingRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      console.log(e);
      setDraggingRect(
        (prev) =>
          prev && {
            ...prev,
            left: e.clientX,
            top: e.clientY,
          }
      );

      //  setDraggingRect(draggingEl.ref.current.getBoundingClientRect());

      window.addEventListener("mousemove", handler);

      return () => window.removeEventListener("mousemove", handler);
    };
  }, [draggingEl]);

  const onElementDragStart = useCallback(
    (val: CurrentDraging | null) => setDraggingEl(val),
    []
  );

  console.log(draggingRect);

  return (
    <Stack
      direction="row"
      sx={{
        alignItems: "center",
        gap: theme.spacing(2),
        width: "min-content",
      }}
    >
      <CategoryHeap
        onElementDragStart={onElementDragStart}
        {...heap}
        items={distribution.heap}
      />
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          flexDirection: "column",
          gap: theme.spacing(2),
          width: "100%",
        }}
      >
        {categories.map((category) => (
          <CategoryHeap
            onElementDragStart={onElementDragStart}
            key={category.value}
            {...category}
            items={distribution[category.value] || []}
          />
        ))}
      </Box>
      {draggingEl && <Item {...draggingEl.item} draggingRect={draggingRect} />}
    </Stack>
  );
};

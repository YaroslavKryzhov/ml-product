import styled from "@emotion/styled";
import { Box, Stack } from "@mui/material";
import { theme } from "globalStyle/theme";
import React, { useCallback, useEffect, useState } from "react";
import SwipeLeftIcon from "@mui/icons-material/SwipeLeft";

const HeapBox = styled.div<{ isHeap?: boolean; isDragHover?: boolean }>`
  width: 300px;
  height: ${({ isHeap }) => (isHeap ? 240 : 120)}px;
  border: ${theme.additional.borderWidth}px solid ${theme.palette.primary.main};
  border-radius: ${theme.shape.borderRadiusRound}px;
  overflow: hidden;
  opacity: ${({ isDragHover }) => (isDragHover ? 0.5 : 1)};
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
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
  fixedX?: number;
  fixedY?: number;
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
  height: min-content;
  opacity: ${({ isDragging }) => (isDragging ? 0.3 : 1)};

  ${({ fixedX, fixedY }) =>
    fixedX &&
    fixedY &&
    `position: fixed; pointer-events: none; left: ${fixedX}px; top: ${fixedY}px;`}

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

type CategoryItem = { value: string; label: string; singleCapacity?: boolean };

export type Distribution = {
  heap: string[];
  [key: string]: string[];
};

type Coords = { x: number; y: number };

const Item: React.FC<
  CategoryItem & {
    onElementDragStart?: (val: CategoryItem | null) => void;
    onItemDrop: (val: CategoryItem) => void;
  }
> = (props) => {
  const [isDragging, setIsDragging] = useState(false);
  const [initialRectCoords, setInitialRectCoords] = useState<DOMRect | null>(
    null
  );
  const [initialMouseCoords, setInitialMouseCoords] = useState<Coords | null>(
    null
  );
  const [mouseCoords, setMouseCoords] = useState<Coords | null>(null);

  useEffect(() => {
    if (isDragging) {
      const handler = () => {
        setIsDragging(false);
        props.onItemDrop(props);
        props.onElementDragStart && props.onElementDragStart(null);
        setInitialRectCoords(null);
        setInitialMouseCoords(null);
        setMouseCoords(null);
      };

      const moveHandler = (e: MouseEvent) => {
        setMouseCoords({ x: e.clientX, y: e.clientY });
      };

      window.addEventListener("mouseup", handler);
      window.addEventListener("mousemove", moveHandler);

      return () => {
        window.removeEventListener("mouseup", handler);
        window.removeEventListener("mousemove", moveHandler);
      };
    }
  }, [isDragging, props]);

  return (
    <>
      <ItemWrapper
        isDragging={isDragging}
        onMouseDown={(e: React.MouseEvent) => {
          setInitialRectCoords(e.currentTarget.getBoundingClientRect());
          setInitialMouseCoords({ x: e.clientX, y: e.clientY });
          setIsDragging(true);
          props.onElementDragStart && props.onElementDragStart(props);
        }}
      >
        {props.label}
        <SwipeLeftIcon sx={{ fontSize: theme.typography.caption.fontSize }} />
      </ItemWrapper>
      {isDragging && mouseCoords && (
        <ItemWrapper
          fixedX={
            initialRectCoords!.left! +
            (mouseCoords!.x! - initialMouseCoords!.x!)
          }
          fixedY={
            initialRectCoords!.top! + (mouseCoords!.y! - initialMouseCoords!.y!)
          }
        >
          {props.label}
          <SwipeLeftIcon sx={{ fontSize: theme.typography.caption.fontSize }} />
        </ItemWrapper>
      )}
    </>
  );
};

const CategoryHeap: React.FC<
  CategoryItem & {
    items: string[];
    draggingItem: CategoryItem | null;
    onElementDragStart: (val: CategoryItem | null) => void;
    onElementDraggedInto: (category: string | null) => void;
    onItemDrop: (val: CategoryItem) => void;
  }
> = ({
  value,
  label,
  singleCapacity,
  items,
  onElementDragStart,
  draggingItem,
  onElementDraggedInto,
  onItemDrop,
}) => {
  const [isMouseOver, setIsMouseOver] = useState(false);

  return (
    <HeapBox
      isDragHover={
        isMouseOver &&
        !!draggingItem?.value &&
        !items.includes(draggingItem.value)
      }
      onMouseOver={() => {
        draggingItem && onElementDraggedInto(value);
        setIsMouseOver(true);
      }}
      onMouseLeave={() => setIsMouseOver(false)}
      isHeap={value === "heap"}
    >
      <HeapName>{label + (singleCapacity ? " (x1)" : "")}</HeapName>
      <HeapElements>
        {items.map((item) => (
          <Item
            onItemDrop={onItemDrop}
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
  const [draggingItem, setDraggingItem] = useState<CategoryItem | null>(null);
  const [draggingCategory, setDraggingCategory] = useState<string | null>(null);

  const onElementDragStart = useCallback(
    (val: CategoryItem | null) => setDraggingItem(val),
    []
  );

  const onItemDrop = useCallback(
    (val: CategoryItem) => {
      const dragCatObj = categories.find((x) => x.value === draggingCategory);

      return (
        draggingCategory &&
        !(
          dragCatObj?.singleCapacity && distribution[draggingCategory].length
        ) &&
        !distribution[draggingCategory].includes(val.value) &&
        distributionChange(
          Object.fromEntries(
            Object.entries(distribution).map(([key, values]) =>
              values.includes(val.value)
                ? [key, values.filter((x) => x !== val.value)]
                : key === draggingCategory
                ? [key, [...values, val.value]]
                : [key, values]
            )
          ) as Distribution
        )
      );
    },
    [draggingCategory, distribution]
  );

  return (
    <Stack
      direction="row"
      sx={{
        alignItems: "flex-start",
        gap: theme.spacing(2),
        width: "min-content",
      }}
    >
      <CategoryHeap
        onElementDraggedInto={setDraggingCategory}
        onItemDrop={onItemDrop}
        draggingItem={draggingItem}
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
        }}
      >
        {categories.map((category) => (
          <CategoryHeap
            onItemDrop={onItemDrop}
            onElementDraggedInto={setDraggingCategory}
            draggingItem={draggingItem}
            onElementDragStart={onElementDragStart}
            key={category.value}
            {...category}
            items={distribution[category.value] || []}
          />
        ))}
      </Box>
    </Stack>
  );
};

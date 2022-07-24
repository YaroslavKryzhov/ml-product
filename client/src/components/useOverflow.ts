import { useEffect, useRef, useState } from "react";

export const useOverflow = <T extends HTMLElement>() => {
  const [isOverflow, setIsOverflow] = useState<boolean>(false);
  const elRef = useRef<T>(null);

  useEffect(() => {
    if (elRef.current)
      setIsOverflow(
        elRef.current.clientWidth >=
          (elRef.current.parentElement?.clientWidth || 0)
      );
  });

  return { isOverflow, elRef };
};

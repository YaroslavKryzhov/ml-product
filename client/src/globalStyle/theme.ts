import { createTheme, ThemeOptions } from "@mui/material/styles";

const themeOptions: ThemeOptions = {
  palette: {
    primary: {
      main: "#24292f",
    },
    secondary: {
      main: "#f6f8fa",
    },
  },
  typography: {
    fontSize: 20,
    fontFamily: "Jost",
    htmlFontSize: 20,
  },
};

export const theme = createTheme(themeOptions);

export const withOpacity = (
  colorHex: string,
  alpha: number
): string | never => {
  let result: string | number = "";
  let component = [] as string[];

  if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(colorHex)) {
    component = colorHex.substring(1).split("");

    if (component.length === 3) {
      component = [
        component[0],
        component[0],
        component[1],
        component[1],
        component[2],
        component[2],
      ];
    }
    result = `0x${component.join("")}`;

    /* eslint-disable no-bitwise */
    return `rgba(${[
      ((result as unknown as number) >> 16) & 255,
      ((result as unknown as number) >> 8) & 255,
      (result as unknown as number) & 255,
    ].join(",")}, ${alpha})`;
    /* eslint-enable no-bitwise */
  }
  throw new Error("Bad Hex");
};

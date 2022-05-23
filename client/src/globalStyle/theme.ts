import { createTheme, ThemeOptions } from "@mui/material/styles";

declare module "@mui/material/styles" {
  interface Theme {
    additional: {
      borderWidth: number;
      timeFormat: string;
    };
    shape: {
      borderRadius: number;
      borderRadiusRound: number;
    };
  }
  interface ThemeOptions {
    additional: {
      borderWidth: number;
      timeFormat: string;
    };
    shape: {
      borderRadiusRound: number;
      borderRadius: number;
    };
  }
}

const themeOptions: ThemeOptions = {
  palette: {
    primary: {
      main: "#24292f",
    },
    secondary: {
      main: "#f6f8fa",
      light: "rgb(238 245 249);",
    },
    success: {
      main: "#83d344",
    },
    info: {
      main: "#8884d8",
      dark: "#7c40df",
      light: "#e4e2ff",
    },
  },
  typography: {
    fontSize: 20,
    fontFamily: "Jost",
    htmlFontSize: 20,
  },
  shape: {
    borderRadius: 4,
    borderRadiusRound: 30,
  },
  additional: { borderWidth: 1, timeFormat: "DD.MM.YYYY (HH:mm)" },
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

import React, { createContext } from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ListItemIcon from "@mui/material/ListItemIcon";
import MuiListItemText, { ListItemTextProps } from "@mui/material/ListItemText";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import {
  AppBar,
  DrawerHeader,
  IconButtonCustom,
  Main,
  MENU_WIDTH,
} from "./styled";
import { styled } from "@mui/material";
import MuiListItemButton, {
  ListItemButtonProps,
} from "@mui/material/ListItemButton";
import {
  AppPage,
  AuthPage,
  CompositionPage,
  DocumentPage,
  WorkPage,
} from "ducks/reducers/types";
import { Documents } from "./Documents";
import { Compositions } from "./Compositions";
import { Matcher, pathify, useAppDispatch } from "ducks/hooks";
import LogoutIcon from "@mui/icons-material/Logout";
import { setDialog } from "ducks/reducers/dialog";
import { useNavigate } from "react-router-dom";
import { Route, Routes, useMatch } from "react-router";
import { T } from "ramda";
import { theme } from "globalStyle/theme";
import BarChartIcon from "@mui/icons-material/BarChart";

const ListItemButton = styled((props: ListItemButtonProps) => (
  <MuiListItemButton {...props} />
))(() => ({
  "&.Mui-selected": {
    backgroundColor: theme.palette.primary.light,
  },
  "&:hover": {
    backgroundColor: theme.palette.primary.dark,
  },
}));

const ListItemText: React.FC<ListItemTextProps> = (props) => (
  <MuiListItemText
    {...props}
    primaryTypographyProps={{ variant: "body2", color: "secondary" }}
  />
);

export const MenuContext = createContext({ menuOpened: false });

export const Workplace: React.FC = () => {
  const [open, setOpen] = React.useState(false);
  const isDocs = !!useMatch(
    pathify([AppPage.Workplace, WorkPage.Documents], { matcher: Matcher.start })
  );
  const isCompositions = !!useMatch(
    pathify([AppPage.Workplace, WorkPage.Compositions], {
      matcher: Matcher.start,
    })
  );
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar open={open}>
        <Toolbar sx={{ justifyContent: open ? "flex-end" : "space-between" }}>
          <IconButtonCustom
            color="secondary"
            onClick={() => setOpen(true)}
            edge="start"
            sx={{
              mr: 2,
              ...(open && { display: "none" }),
            }}
          >
            <MenuIcon />
          </IconButtonCustom>
          <IconButtonCustom
            color="secondary"
            onClick={() =>
              dispatch(
                setDialog({
                  text: "Вы действительно хотите выйти?",
                  onAccept: async () => {
                    localStorage.authToken = "";
                    navigate(pathify([AppPage.Authentication, AuthPage.auth]));
                  },
                  title: "Выход",
                  onDismiss: T,
                })
              )
            }
            edge="end"
          >
            <LogoutIcon />
          </IconButtonCustom>
        </Toolbar>
      </AppBar>
      <Drawer
        elevation={3}
        sx={{
          width: MENU_WIDTH,
          "& .MuiDrawer-paper": {
            width: MENU_WIDTH,
            backgroundColor: "primary.main",
          },
        }}
        variant="persistent"
        open={open}
      >
        <DrawerHeader>
          <IconButtonCustom
            sx={{
              "&:hover": {
                backgroundColor: "primary.light",
              },
            }}
            onClick={() => setOpen(false)}
          >
            <ChevronLeftIcon color="secondary" />
          </IconButtonCustom>
        </DrawerHeader>
        <Divider sx={{ backgroundColor: "primary.light" }} />
        <List>
          <ListItemButton
            onClick={() => {
              navigate(
                pathify([WorkPage.Documents, DocumentPage.List], {
                  relative: true,
                })
              );
            }}
            selected={isDocs}
          >
            <ListItemIcon>
              <FormatListBulletedIcon color="secondary" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Документы" />
          </ListItemButton>
          <ListItemButton
            onClick={() => {
              navigate(
                pathify([WorkPage.Compositions, CompositionPage.List], {
                  relative: true,
                })
              );
            }}
            selected={isCompositions}
          >
            <ListItemIcon>
              <BarChartIcon color="secondary" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Композиции" />
          </ListItemButton>
        </List>
      </Drawer>
      <Main open={open}>
        <MenuContext.Provider value={{ menuOpened: open }}>
          <Box
            sx={{
              maxWidth: 1480,
              marginLeft: "auto",
              marginRight: "auto",
              width: "100%",
            }}
          >
            <Routes>
              <Route
                path={pathify([WorkPage.Documents], {
                  matcher: Matcher.start,
                })}
                element={<Documents />}
              />
              <Route
                path={pathify([WorkPage.Compositions], {
                  matcher: Matcher.start,
                })}
                element={<Compositions />}
              />
            </Routes>
          </Box>
        </MenuContext.Provider>
      </Main>
    </Box>
  );
};

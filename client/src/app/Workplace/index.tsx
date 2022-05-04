import React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import {
  AppBar,
  DrawerHeader,
  IconButtonCustom,
  Main,
  MENU_WIDTH,
} from "./styled";
import { ListItemButton } from "@mui/material";
import { always, cond, equals, T } from "ramda";
import { DocumentPage, WorkPage } from "ducks/reducers/types";
import { Documents } from "./Documents";
import { changeDocumentPage } from "ducks/reducers/documents";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { changeWorkPage, logout } from "ducks/reducers/main";
import { WorkPageHeader } from "./common/WorkPageHeader";
import LogoutIcon from "@mui/icons-material/Logout";
import { ShowDialog } from "components/Dialog";

export const Workplace: React.FC = () => {
  const [open, setOpen] = React.useState(false);
  const { workPage } = useSESelector((state) => state.main);
  const dispatch = useAppDispatch();

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
              ShowDialog({
                text: "Вы действительно хотите выйти?",
                onAccept: () => dispatch(logout()),
                title: "Выход",
              })
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
            sx={{
              "&.Mui-selected": {
                backgroundColor: "primary.light",
              },
              "&.Mui-selected:hover": {
                backgroundColor: "primary.dark",
              },
            }}
            selected
          >
            <ListItemIcon>
              <FormatListBulletedIcon color="secondary" fontSize="small" />
            </ListItemIcon>
            <ListItemText
              onClick={() => {
                dispatch(changeWorkPage(WorkPage.Documents));
                dispatch(changeDocumentPage(DocumentPage.List));
              }}
              primary="Документы"
              primaryTypographyProps={{ variant: "body2", color: "secondary" }}
            />
          </ListItemButton>
        </List>
      </Drawer>
      <Main open={open}>
        <WorkPageHeader />
        {cond<WorkPage[], JSX.Element>([
          [equals<WorkPage>(WorkPage.Documents), always(<Documents />)],
          [T, always(<Documents />)],
        ])(workPage)}
      </Main>
    </Box>
  );
};

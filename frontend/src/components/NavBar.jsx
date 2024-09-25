import * as React from "react";
import Drawer from "@mui/material/Drawer";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import Person2Icon from "@mui/icons-material/Person2";
import LogoutIcon from "@mui/icons-material/Logout";
import AddchartIcon from "@mui/icons-material/Addchart";
import SchoolIcon from "@mui/icons-material/School";
import GroupsIcon from "@mui/icons-material/Groups";
import SettingsIcon from "@mui/icons-material/Settings";
import PlaylistAddIcon from "@mui/icons-material/PlaylistAdd";
import NavButton from "./NavButton";
import { styled } from "@mui/material/styles";
import { canAdd, getHighestUserType, getUserType, isAdmin } from "../helpers/helper";
import UserTypeSelection from "./UserTypeSelection";
import { useTheme } from "@mui/material/styles";
import useMediaQuery from "@mui/material/useMediaQuery";
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';

// Academic
// Courses
// Add Course
// Projects
// Add Projects
// Profile
// Students

// Student
//	Courses
//	All Projects
//	My Projects
//	My Profile
//	Other Students

// Admin
//	Courses
//	Add Course
//	Projects
//	Add Projects
//	Students
//	Profile

// https://mui.com/material-ui/react-drawer/
const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  transition: theme.transitions.create(["margin", "width"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginRight: drawerWidth,
  }),
}));

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-start",
}));

function NavBar() {
  const [drawOpen, setDrawOpen] = React.useState(false);
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.down(535));

  const openDraw = () => {
    setDrawOpen(true);
  };

  const closeDraw = () => {
    setDrawOpen(false);
  };

  function navList() {
    return (
      <>
        <List>
          <NavButton
            path="/"
            label="Logout"
            key="logout"
            icon={<LogoutIcon />}
          />
          <NavButton
            path="/settings/account-preference"
            label="Settings"
            key="settings"
            icon={<SettingsIcon />}
          />
          <NavButton
            path="/profile"
            label="Profile"
            key="profile"
            icon={<Person2Icon />}
          />
          <NavButton
            path="/project-dashboard"
            label="Projects"
            key="projects"
            icon={<AddchartIcon />}
          />
          <NavButton
            path="/course-dashboard"
            label="Courses"
            key="courses"
            icon={<SchoolIcon />}
          />
          {canAdd() && (
            <NavButton
              path="/add-project"
              label="Add Project"
              key="addProject"
              icon={<PlaylistAddIcon />}
            />
          )}
          {canAdd() && (
            <NavButton
              path="/add-course-menu"
              label="Add Course"
              key="addCourse"
              icon={<PlaylistAddIcon />}
            />
          )}
          
          {
            getUserType() == 'student'
            &&
            <NavButton
              path="/similar-students"
              label="Students"
              key="students"
              icon={<GroupsIcon />}
            />
          }
            
          {isAdmin() && 
          <NavButton 
            path='/admin' 
            label="Admin Centre" 
            key="adminCentre" 
            icon={<AdminPanelSettingsIcon />} 
          />}

        </List>
      </>
    );
  }

  return (
    <>
      <AppBar
        position="fixed"
        open={drawOpen}
        sx={{
          backgroundColor: "#426B1F",
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap sx={{ flexGrow: 1 }}>
            Application Name
          </Typography>
          <div
            className="top-buttons"
            style={{ display: matches ? "none" : "flex" }}
          >
            {canAdd() && (
              <NavButton
                edge="end"
                path="/add-project"
                label="Add Project"
                key="addProject"
                icon={<PlaylistAddIcon sx={{ ml: 2.5, color: "white" }} />}
              />
            )}
            {canAdd() && (
              <NavButton
                edge="end"
                path="/add-course-menu"
                label="Add Course"
                key="addCourse"
                icon={<PlaylistAddIcon sx={{ ml: 2.5, color: "white" }} />}
              />
            )}
            {!canAdd() && (
              <NavButton
                path="/course-dashboard"
                label="Courses"
                key="courses"
                icon={<SchoolIcon sx={{ ml: 2.5, color: "white" }} />}
              />
            )}
            {!canAdd() && (
              <NavButton
                path="/project-dashboard"
                label="Projects"
                key="projects"
                icon={<AddchartIcon sx={{ ml: 2.5, color: "white" }} />}
              />
            )}
          </div>
          <IconButton
            color="inherit"
            edge="end"
            onClick={openDraw}
            sx={{ ...(drawOpen && { display: "none" }) }}
          >
            <MenuIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: 240,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: 240,
          },
        }}
        variant="persistent"
        anchor="right"
        open={drawOpen}
      >
        <DrawerHeader>
          <IconButton onClick={closeDraw}>
            <ChevronRightIcon />
          </IconButton>
        </DrawerHeader>
        <Divider />
        {navList()}
        <Divider />
        {getHighestUserType() !== "student" && <UserTypeSelection />}
      </Drawer>
    </>
  );
}

export default NavBar;

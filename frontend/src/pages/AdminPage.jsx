import React from 'react';
import NavBar from '../components/NavBar';

import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import NavButton from '../components/NavButton';

import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import DescriptionIcon from '@mui/icons-material/Description';
import { useNavigate } from 'react-router-dom';
import { isAdmin } from '../helpers/helper';
import { useGlobalState } from '../components/GlobalReloadProvider';

function navList() {
    return (
      <>
        <List>
          <NavButton path='/admin/dashboard' label='Dashboard' key='dashboard' icon={<DashboardIcon />}/>
          <NavButton path='/admin/people' label='People' key='people' icon={<PeopleIcon />}/>
          <NavButton path='/admin/courses' label='Courses' key='courses' icon={<LibraryBooksIcon />}/>
          <NavButton path='/admin/projects' label='Projects' key='projects' icon={<DescriptionIcon />}/>
        </List>
      </>
    )
}

export default function AdminPage(props) {
    const drawerWidth = 240;

    const navigate = useNavigate()

    const { globalReload} = useGlobalState();

    React.useEffect(() => {
        async function checkIsAdmin() {
            if (!isAdmin()) {
                navigate('/profile')
            }
        }
        checkIsAdmin()
    }, [globalReload])

    return (
    <div>
        <NavBar />
        <Box sx={{ display: "flex" }}>
            <CssBaseline />
            <Drawer
                variant="permanent"
                sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: {
                    width: drawerWidth,
                    boxSizing: "border-box",
                },
                }}
            >
                <Toolbar />
                <Box sx={{ overflow: "auto" }}>
                <Typography
                    variant="h4"
                    component="h4"
                    sx={{
                    mt: 2,
                    mb: 1.5,
                    paddingLeft: 2,
                    }}
                >
                    Admin Centre
                </Typography>
                <Divider />
                {navList()}
                </Box>
            </Drawer>
            
            <Box
                component="main"
                sx={{ flexGrow: 1, p: 3,  }}
            >
                {props.content}
            </Box>
        </Box>
    </div>
    )
}
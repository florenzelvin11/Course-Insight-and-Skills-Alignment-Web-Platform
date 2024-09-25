import React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import NavButton from './NavButton';
import { Person2 as Person2Icon, Lock as LockIcon } from '@mui/icons-material';
import EditAccountPreference from './EditAccountPreference';
import { useLocation } from 'react-router-dom';
import EditEmail from './EditEmail';
import AdminSetUserType from './AdminSetUserType';
import EditPassword from './EditPassword';
import { getUserData, apiCall, setUserData } from '../helpers/helper';
import LoadingScreen from '../components/LoadingScreen';
import ProfileSetPrivacy from './ProfileSetPrivacy';

const drawerWidth = 240;

function navList() {
  return (
    <>
      <List>
        <NavButton path='/settings/account-preference' label='Account preferences' key='accountPreferences' icon={<Person2Icon />}/>
        <NavButton path='/settings/sign-in-and-security' label='Sign in & security' key='signInSecurity' icon={<LockIcon />}/>
        {getUserData()?.userType === "admin" && <NavButton path='/settings/admin/set-user-type' label='Set user type' key='setusertype' icon={<Person2Icon />}/>}
      </List>
    </>
  )
}

export default function SettingsSection() {
  
  const [section, setSection] = React.useState(1)
  
  const location = useLocation()
  
  React.useEffect(() => {
    switch (location.pathname) {
      case '/settings/account-preference':
        setSection(1)
        break
      case '/settings/sign-in-and-security':
        setSection(2)
        break
      case '/settings/admin/set-user-type':
        setSection(3)
        break
      default:
        setSection(1)
    }
  }, [location])

  const [isLoading, setIsLoading] = React.useState(true)
  const localProfileData = getUserData()?.profileData;
  const [ profileData, setProfileData ] = React.useState(null);

  React.useEffect(() => {
      async function getProfileData() {
        try {
          const response = await apiCall('GET', '/user/profile')
          if (!response.error) {
              setUserData({ profileData: {...localProfileData, ...response}})
              setProfileData(response);
              setIsLoading(false)
          }
          return response
        } catch(e) {
          //
        }
      }
      getProfileData()
  }, [])

  return (
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
            variant="h3"
            component="h2"
            sx={{
              mt: 2,
              mb: 1.5,
              paddingLeft: 2,
            }}
          >
            Settings
          </Typography>
          <Divider />
          {navList()}
        </Box>
      </Drawer>
      {
        isLoading
        ? 
        <LoadingScreen />
        :
        <Box
          component="main"
          sx={{ flexGrow: 1, p: 3, }}
        >
          <Toolbar />
          {
            section === 1 
            &&
            <EditAccountPreference
              navigateTo={() => {}}
            />
          }

          {
            section === 2
            &&
            <>
            <EditEmail email={profileData?.email} />

            <EditPassword />
            
            <ProfileSetPrivacy profileData={profileData} />
            </>
          }

          {
            (section === 3)
            &&
            <>
            <AdminSetUserType />
            </>
          }
        </Box>
      }
    </Box>
  );
}

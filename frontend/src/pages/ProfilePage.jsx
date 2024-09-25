import React, { useEffect } from 'react';
import { Box, useMediaQuery } from '@mui/material';
import NavBar from '../components/NavBar';
import { apiCall, getUserData, setUserData } from '../helpers/helper';
import LoadingScreen from '../components/LoadingScreen';
import UserWidget from '../components/UserWidget';
import ProfileCourseWidget from '../components/ProfileCourseWidget';
import ProfileSkillsWidget from '../components/ProfileSkillsWidget';
import ProfileKnowledgeWidget from '../components/ProfileKnowledgeWidget';
import ProfileProjectWidget from '../components/ProfileProjectWidget';
import EditProfileIntro from '../components/EditProfileIntro';
import AddProfileCourse from '../components/AddProfileCourse';
import SimilarStudentsWidget from '../components/SimilarStudentsWidget';
import { useGlobalState,  } from '../components/GlobalReloadProvider';

function ProfilePage() {
    const isNonMobileScreen = useMediaQuery("(min-width: 1000px)");

    const userType = getUserData()?.userType;

    const { globalReload } = useGlobalState();
    const [isLoading, setIsLoading] = React.useState(true)
    
    const [open, setOpen] = React.useState({
        editIntro: false,
        addCourse: false, 
    });

    const localProfileData = getUserData()?.profileData;
    const [profileData, setProfileData] = React.useState(localProfileData || null)

    React.useEffect(() => {
        async function getProfileData() {
            try {
                const response = await apiCall('GET', '/user/profile')
                if (!response.error) {
                    setProfileData(response)
                    setUserData({profileData: {...localProfileData, ...response}})
                    setIsLoading(false)
                }
                return response
            } catch(e) {
                //
            }
        }
        getProfileData()
    }, [open, globalReload])

    useEffect(() => {
        setProfileData({...getUserData()?.profileData})
    }, [open])

    const handleClickOpen = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : true}));
    };

    const handleClose = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : false}));
    };

    const handleSubmit = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : false}));
        setIsLoading(true)
    }

    return (
    <div>
        <NavBar />
        {
            isLoading ?
            <LoadingScreen />
            : 
            
            <div className='container'>
            <Box
                mt="100px"
                width="90%"
                maxWidth="2000px"
                padding="1rem 0"
                display={isNonMobileScreen ? "flex" : "block"}
                gap="0.75rem"
                justifyContent="center"
            >
                <Box flexBasis={isNonMobileScreen ? "26%" : undefined}>
                    <UserWidget 
                        id="user-wiget" 
                        profileData={profileData} 
                        userType={userType}
                        handleClickOpen={() => handleClickOpen("editIntro")}
                    />
                    <Box m="2rem 0" />  
                </Box>
                {
                    (userType !==  "admin")
                    &&
                    <Box flexBasis={isNonMobileScreen ? "46%" : undefined}>
                    <ProfileCourseWidget zID={profileData.zID} userType={userType} handleClickOpen={() => handleClickOpen("addCourse")}/>
                    <Box m="2rem 0" />
                    {
                        getUserData()?.userType !== 'academic'
                        &&
                        <>
                        <ProfileProjectWidget zID={profileData.zID} userType={userType} handleClickOpen={() => handleClickOpen("addProject")} />
                        <Box m="2rem 0" />
                        </>
                    }

                    {
                        (getUserData()?.userType === "student")
                        &&
                        <>
                        <ProfileKnowledgeWidget zID={profileData.zID} userType={userType}/>
                        <Box m="2rem 0" />
                        <ProfileSkillsWidget zID={profileData.zID} userType={userType}/>
                        <Box m="2rem 0" />
                        </>
                    }
                    </Box>
                }
                {
                    (getUserData()?.userType === "student")
                    &&
                    <Box flexBasis={isNonMobileScreen ? "26%" : undefined} minWidth="300px">
                        <SimilarStudentsWidget zID={profileData.zID} />
                        <Box m="2rem 0" />
                    </Box>
                }
            </Box>
            <EditProfileIntro 
                id="edit-profile-intro"
                open={open.editIntro}
                profileData={profileData}
                handleClose={() => handleClose("editIntro")}
                handleSubmit={() => handleSubmit("editIntro")}
            />
            <AddProfileCourse
                id="add-profile-course"
                open={open.addCourse}
                zID={profileData.zID}
                userType={userType}
                handleClose={() => handleClose("addCourse")}
                handleSubmit={() => handleSubmit("addCourse")}
            />
            </div>
        }
    </div>
    );
}

export default ProfilePage;

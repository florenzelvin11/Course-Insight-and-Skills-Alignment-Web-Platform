import React from 'react';
import { Box, useMediaQuery } from '@mui/material';
import NavBar from '../components/NavBar';
import { apiCall, getUserData } from '../helpers/helper';
import LoadingScreen from '../components/LoadingScreen';
import UserWidget from '../components/UserWidget';
import ProfileCourseWidget from '../components/ProfileCourseWidget';
import ProfileSkillsWidget from '../components/ProfileSkillsWidget';
import ProfileKnowledgeWidget from '../components/ProfileKnowledgeWidget';
import ProfileProjectWidget from '../components/ProfileProjectWidget';
import EditProfileIntro from '../components/EditProfileIntro';
import AddProfileCourse from '../components/AddProfileCourse';
import { useParams } from 'react-router-dom';
import { useGlobalState } from '../components/GlobalReloadProvider';
import PageHeading from '../components/PageHeading';

function PublicProfilePage() {
    const isNonMobileScreen = useMediaQuery("(min-width: 1000px)");
    
    const isAdmin = (getUserData()?.userType === "admin")

    const params = useParams();
    const { globalReload, setGlobalReload } = useGlobalState();

    const [open, setOpen] = React.useState({
        editIntro: false,
        addCourse: false, 
    });
    
    const [isLoading, setIsLoading] = React.useState(true)
    const [profileData, setProfileData] = React.useState(null)

    React.useEffect(() => {
        async function getProfileData() {
            try {
                const response = await apiCall('GET', `/user/profile/${params.userType}?zID=${params.zID}`)
                // const response = successfulResponse()
                if (!response.error) {
                    setProfileData(response)
                    setIsLoading(false)
                }
                return response
            } catch(e) {
                //
            }
        }
        getProfileData()
    }, [globalReload])

    const handleClickOpen = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : true}));
    };

    const handleClose = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : false}));
    };

    const handleSubmit = (popUp) => {
        setOpen((prevOpen) => ({...prevOpen, [popUp] : false}));
        setIsLoading(true)
        setGlobalReload(!globalReload);
    }

    return (
    <div>
        <NavBar />
        <PageHeading 
            backButtonName={"Back"}
            backPath={-1}
        />
        {
            isLoading ?
            <LoadingScreen />
            : 
            <div className='container'>
            <Box
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
                        userType={params.userType}
                        handleClickOpen={() => handleClickOpen("editIntro")}
                        public={!isAdmin}
                    />
                    <Box m="2rem 0" />  
                </Box>
                {
                    (!profileData.private || isAdmin)
                    &&
                    <Box flexBasis={isNonMobileScreen ? "46%" : undefined}>
                        <ProfileCourseWidget zID={profileData.zID} userType={params.userType} handleClickOpen={() => handleClickOpen("addCourse")} public={!isAdmin}/>
                        <Box m="2rem 0" />
                        { 
                            params.userType !== 'academic'
                            &&
                            <>
                            <ProfileProjectWidget zID={profileData.zID} userType={params.userType} public={!isAdmin}/>
                            <Box m="2rem 0" />
                            </>
                        }
                        {
                            params.userType === 'student'
                            &&
                            <>
                            <ProfileKnowledgeWidget zID={profileData.zID} userType={params.userType}/>
                            <Box m="2rem 0" />
                            <ProfileSkillsWidget zID={profileData.zID} userType={params.userType}/>
                            <Box m="2rem 0" />
                            </>
                        }
                    </Box>
                }
            </Box>
            {
                (isAdmin)
                &&
                <>
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
                    zID={params.zID}
                    userType={params.userType}
                    handleClose={() => handleClose("addCourse")}
                    handleSubmit={() => handleSubmit("addCourse")}
                />
                </>
            }
            </div>
        }
    </div>
    );
}

export default PublicProfilePage;

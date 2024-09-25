import React from 'react';
import PageHeading from '../components/PageHeading';
import EditProfileSignInSecurity from '../components/EditProfileSignInSecurity';
import { useParams } from 'react-router-dom';
import NavBar from '../components/NavBar';
import LoadingScreen from '../components/LoadingScreen';
import { apiCall } from '../helpers/helper';
import { useGlobalState } from '../components/GlobalReloadProvider';

export default function AdminProfileSecurityPage() {
    
    const params = useParams()
    const { globalReload } = useGlobalState()
    
    const [isLoading, setIsLoading] = React.useState(true)
    const [profileData, setProfileData] = React.useState(null)

    React.useEffect(() => {
        async function getProfileData() {
            try {
                const response = await apiCall('GET', `/user/profile?zID=${params.zID}`)
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

    return (
        <>
        <NavBar />
        {
            isLoading 
            ?
            <LoadingScreen />
            :
            <>
            <PageHeading 
                backButtonName="Back"
                backPath={-1}
                title={profileData.firstName + ' ' + profileData.lastName}
            />
            
            <EditProfileSignInSecurity profileData={profileData} />

            </>
        }
        </>
    )
}
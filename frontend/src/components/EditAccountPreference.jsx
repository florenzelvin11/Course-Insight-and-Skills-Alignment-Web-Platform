import React from 'react'
import EditTextField from './EditTextField';
import AuthTextField from './AuthTextField';
import FormButtons from './FormButtons';
import { apiCall, getUserData, setUserData, isValidName } from '../helpers/helper';
import { invalidFirstName, invalidLastName } from '../constants/constants'
import AlertCard from './AlertCard';

export default function EditAccountPreference(props) {
    const localProfileData = getUserData()?.profileData;
    const [profileData, setProfileData] = React.useState({
        zID: localProfileData?.zID || '',
        firstName: localProfileData?.firstName || '',
        lastName: localProfileData?.lastName || '',
        headline: localProfileData?.headline || '',
        summary: localProfileData?.summary || '',
    });
    
    const [prevProfileData, setPrevProfileData] = React.useState(profileData)
    const [alert, setAlert] = React.useState({
        severity: null,
        message: null,
    });

    function setErrorAlert(message) {
        setAlert({severity : "error", message : message})
    }

    function setSuccessAlert(message) {
        setAlert({severity : "success", message : message})
    }

    function resetAlert() {
        setAlert({severity : null, message : null})
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProfileData({ ...profileData, [name]: value }); 
    };
    
    const onSubmit = async () => {
        const requestData = profileData
        const response = await apiCall('PUT', '/user/profile/setaccountpreference', requestData)

        if (!response.error) {
            setUserData({profileData: {...localProfileData, ...profileData}})
            setPrevProfileData(profileData)
            props.navigateTo()
            setSuccessAlert("Changes Saved!")
        } else {
            setErrorAlert(response.error)
        }
        return response
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        // Add code here to submit the updated profile data
        if (!isValidName(profileData.firstName)) {
            setErrorAlert(invalidFirstName)
            return
        }

        if (!isValidName(profileData.lastName)) {
            setErrorAlert(invalidLastName)
            return
        }
        onSubmit()
    };

    const handleCancel = (e) => {
        e.preventDefault()
        props.navigateTo()

        setProfileData(prevProfileData)
        resetAlert()
    }

    return (
        <>
        <div className='central-card pop-up'>
            <form className='edit-form' onSubmit={handleSubmit} style={{borderRadius: '20px', ...props.sx}}>
                <div className='edit-heading'>
                    <h1>
                        {
                            props?.header
                            ||
                            "Edit Account Preference"
                        }
                    </h1>
                </div>
                <AuthTextField onChange={handleInputChange} name="firstName" label="First Name" value={profileData.firstName}/>
                <AuthTextField onChange={handleInputChange} name="lastName" label="Last Name" value={profileData.lastName}/>
                <EditTextField onChange={handleInputChange} name="headline" label="Headline" value={profileData.headline} notRequired />
                <EditTextField onChange={handleInputChange} name="summary" label="Summary" value={profileData.summary} multiline rows={4} notRequired />
                <AlertCard severity={alert.severity} message={alert.message} />
                <FormButtons navigateTo={props.navigateTo} cancel onCancel={handleCancel}/>
            </form>
            
        </div>
        </>
    )
}
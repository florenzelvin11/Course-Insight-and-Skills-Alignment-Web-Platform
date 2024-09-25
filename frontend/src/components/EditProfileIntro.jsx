import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import EditTextField from './EditTextField';
import AuthTextField from './AuthTextField';
import { apiCall, isValidName } from '../helpers/helper';
import AlertCard from './AlertCard';
import { invalidFirstName, invalidLastName } from '../constants/constants'
import { useTheme, Box } from '@mui/material';

export default function EditProfileIntro(props) {

    const { palette } = useTheme()

    const [profileData, setProfileData] = React.useState({
        zID: props.profileData?.zID || '',
        firstName: props.profileData?.firstName || '',
        lastName: props.profileData?.lastName || '',
        headline: props.profileData?.headline || '',
        summary: props.profileData?.summary || '',
        imageURL: props.profileData?.imageURL || '',
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
        const response = await apiCall('PUT', '/user/profile/edit-intro', requestData)

        if (!response.error) {
            setPrevProfileData(profileData)
            setSuccessAlert("Changes Saved!")
            resetAlert()
            props.handleSubmit()
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
        props.handleClose()
        setProfileData(prevProfileData)
        resetAlert()
    }

  return (
    <div>
      <Dialog
        open={props.open}
        onClose={props.handleClose}
        scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle 
            id="scroll-dialog-title"
            bgcolor={"#f2f2e4"}
        >Edit Profile Intro</DialogTitle>
        <DialogContent 
            dividers={true} 
            sx={{
                backgroundColor: palette.secondary.main,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            <Box>
                <AuthTextField onChange={handleInputChange} name="firstName" label="First Name" value={profileData.firstName} sx={{width: '100%'}}/>
                <AuthTextField onChange={handleInputChange} name="lastName" label="Last Name" value={profileData.lastName} sx={{width: '100%'}}/>
                <EditTextField onChange={handleInputChange} name="headline" label="Headline" value={profileData.headline} notRequired sx={{width: '100%'}}/>
                <EditTextField onChange={handleInputChange} name="summary" label="Summary" value={profileData.summary} multiline rows={4} notRequired sx={{width: '100%'}}/>
                <EditTextField onChange={handleInputChange} name="imageURL" label="Profile Image URL" value={profileData.imageURL} notRequired sx={{width: '100%'}}/>
            </Box>
            <AlertCard severity={alert.severity} message={alert.message} />
        </DialogContent>
        <Box bgcolor={"#f2f2e4"}>
            <DialogActions>
                    <Button onClick={handleCancel}>Cancel</Button>
                    <Button onClick={handleSubmit}>Save</Button>
            </DialogActions>
        </Box>
      </Dialog>
    </div>
  );
}

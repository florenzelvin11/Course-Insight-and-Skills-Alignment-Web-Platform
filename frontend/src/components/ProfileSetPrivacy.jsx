import React from 'react'
import FormButtons from './FormButtons'
import { apiCall } from '../helpers/helper'
import DropDownInput from './DropDownInput';
import AlertCard from './AlertCard';

const privacyOptions = [
    {
        label: "Yes",
        value: true
    },
    {
        label: "No",
        value: false
    },
];

export default function ProfileSetPrivacy(props) {
    const { profileData } = props;

    const [privacy, setPrivacy] = React.useState({
        private: profileData?.private,
    })
    
    const [alert, setAlert] = React.useState({
        severity: null,
        message: null,
    });
    
    function resetPrivate() {
        setPrivacy({
            private: profileData?.private,
        })
    }

    function setErrorAlert(message) {
        setAlert({severity : "error", message : message})
    }

    function setSuccessAlert(message) {
        setAlert({severity : "success", message : message})
    }

    function resetAlert() {
        setAlert({severity : null, message : null})
    }

    const onSubmit = async () => {
        const requestData = {
            zID: profileData.zID,
            private: privacy.private
        }
        const response = await apiCall('PUT','/profile/edit/privacy', requestData)
        // const response = {}
        
        if (!response.error) {
            setSuccessAlert('Saved!')
        } else {
            setErrorAlert(response.error)
        }

        return response
    }

    const handleSubmit = (e) => {
        e.preventDefault()

        onSubmit()
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPrivacy({
            [name] : value
        })
    }

    const handleCancel = (e) => {
        e.preventDefault()
        resetPrivate()
        resetAlert()
    }

    return (
        <>
        <div className='central-card'>
            <form className='edit-form' onSubmit={handleSubmit} style={{borderRadius: '20px' }}>
              <div className='edit-heading'>
                <h2>Set Privacy</h2>
              </div>
              <DropDownInput onChange={handleInputChange} name="private" selectedOption={privacy.private} menuItems={privacyOptions} label="Privacy"/>
              <AlertCard severity={alert.severity} message={alert.message} />
              <FormButtons cancel onCancel={handleCancel}/>
            </form>
          </div>
        </>
    )
}
import React from 'react'
import { apiCall } from '../helpers/helper'
import { nonMatchingPasswordErrorMessage } from '../constants/constants';
import AuthTextField from './AuthTextField';
import FormButtons from './FormButtons';
import AlertCard from './AlertCard';

export default function AdminResetPassword(props) {
    const [accountDetail, setAccountDetail] = React.useState({
        zID: props.zID,
        newPassword: '',
        confirmedPassword: ''
    })

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

    const inputChange = (e) => {
        const { name, value } = e.target
        setAccountDetail({...accountDetail, [name]:value})
    }
    
    const onSubmit = async () => {
        const requestData = {
            zID: accountDetail.zID,
            newPassword: accountDetail.newPassword,
        }

        const response = await apiCall('PUT', '/admin/auth/passwordreset', requestData)

        if (!response.error) {
            // alert("Changes Saved")
            setSuccessAlert("Changes Saved!")
        } else {
            setErrorAlert(response.error)
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()

        if (accountDetail.newPassword === accountDetail.confirmedPassword) {
            onSubmit()
            setAccountDetail({
                currentPassword: '',
                newPassword: '',
                confirmedPassword: ''
            })
        } else {
            // alert(nonMatchingPasswordErrorMessage)
            setErrorAlert(nonMatchingPasswordErrorMessage)
        }
    }

    const handleCancel = (e) => {
        e.preventDefault()
        
        // Resets the form
        setAccountDetail({
            currentPassword: '',
            newPassword: '',
            confirmedPassword: ''
        })
        resetAlert()
    }

    return (
        <>
        <div className='central-card'>
            <form className='edit-form' onSubmit={handleSubmit} style={{borderRadius: '20px' }}>
              <div className='edit-heading'>
                <h2>Reset Password</h2>
              </div>
              <AuthTextField type="password" onChange={inputChange} name="newPassword" label="Password" value={accountDetail.newPassword}/>
              <AuthTextField type="password" onChange={inputChange} name="confirmedPassword" label="Confirm Password" value={accountDetail.confirmedPassword} />
              {<AlertCard severity={alert.severity} message={alert.message} />}
              <FormButtons cancel onCancel={handleCancel} />
            </form>
          </div>
        </>
    )
}
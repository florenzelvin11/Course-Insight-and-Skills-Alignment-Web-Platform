import React from 'react'
import AuthTextField from './AuthTextField';
import FormButtons from './FormButtons';
import { apiCall, getUserData, setUserData, isValidEmail } from '../helpers/helper';
import { invalidEmailErrorMessage } from '../constants/constants'
import AlertCard from './AlertCard';

export default function EditEmail(props) {

    const [email, setEmail] = React.useState(props?.email)
    const [prevEmail, setPrevEmail] = React.useState(email)
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
        const { value } = e.target
        setEmail(value)
    }
    
    const onSubmit = async () => {
        const requestData = {
            email : email
        }

        const response = await apiCall('PUT', '/auth/setemail', requestData)
        if (!response.error) {
            setUserData({profileData: {...getUserData()?.profileData, ...requestData}})
            setPrevEmail(email)
            setSuccessAlert('Saved!')
        } else {
            setErrorAlert(response.error)
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (isValidEmail(email)) {
            onSubmit()
        } else {
            setErrorAlert(invalidEmailErrorMessage)
        }
    }

    const handleCancel = (e) => {
        e.preventDefault()
        setEmail(prevEmail)
        resetAlert()
    }

    return (
        <>
        <div className='central-card'>
            <form className='edit-form' onSubmit={handleSubmit} style={{borderRadius: '20px' }}>
                <div className='edit-heading'>
                <h2>Edit Email</h2>
                </div>
                <AuthTextField onChange={inputChange} name="email" label="Email" value={email}/>
                <AlertCard severity={alert.severity} message={alert.message} />
                <FormButtons cancel onCancel={handleCancel} />
            </form>
        </div>
        </>
    )
}
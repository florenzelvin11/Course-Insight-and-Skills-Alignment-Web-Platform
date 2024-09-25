import React from 'react'
import EditTextField from './EditTextField'
import FormButtons from './FormButtons'
import { apiCall } from '../helpers/helper'
import { userTypeOptions } from '../constants/constants'
import DropDownInput from './DropDownInput';
import AlertCard from './AlertCard';

export default function AdminSetUserType(props) {

    const [zUser, setZUser] = React.useState({
        zId: props?.zID,
        userType: ''
    })
    
    const [alert, setAlert] = React.useState({
        severity: null,
        message: null,
    });


    function resetZUser() {
        setZUser({
            zId: '',
            userType: ''
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
        const requestData = zUser
        const response = await apiCall('PUT','/admin/user/edit/usertype', requestData)

        if (!response.error) {
            resetZUser()
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
        setZUser({
            ...zUser, 
            [name] : value
        })
    }

    const handleCancel = (e) => {
        e.preventDefault()

        resetZUser()
        resetAlert()
    }

    return (
        <>
        <div className='central-card'>
            <form className='edit-form' onSubmit={handleSubmit} style={{borderRadius: '20px' }}>
              <div className='edit-heading'>
                <h2>Set User Type</h2>
              </div>
              <EditTextField onChange={handleInputChange} name="zId" label="zId" value={zUser.zId} readOnly={props?.readOnly} />
              <DropDownInput onChange={handleInputChange} name="userType" selectedOption={zUser.userType} menuItems={userTypeOptions} label="User Type"/>
              <AlertCard severity={alert.severity} message={alert.message} />
              <FormButtons cancel onCancel={handleCancel}/>
            </form>
          </div>
        </>
    )
}
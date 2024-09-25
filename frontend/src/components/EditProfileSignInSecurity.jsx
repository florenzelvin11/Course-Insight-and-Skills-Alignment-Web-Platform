import { Box } from '@mui/material';
import React from 'react';
import EditEmail from './EditEmail';
import ProfileSetPrivacy from './ProfileSetPrivacy';
import AdminSetUserType from './AdminSetUserType';
import AdminResetPassword from './AdminEditPassword';

export default function EditProfileSignInSecurity(props) {
    const { profileData } = props
    return (
        <>
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignContent: 'center',
                gap: '0.25rem',
            }}
        >
            <EditEmail email={profileData?.email} />
            <AdminResetPassword zID={profileData.zID} />
            <ProfileSetPrivacy profileData={profileData}/>
            <AdminSetUserType zID={`z${profileData.zID}`} readOnly/>
        </Box>
        </>
    )
}
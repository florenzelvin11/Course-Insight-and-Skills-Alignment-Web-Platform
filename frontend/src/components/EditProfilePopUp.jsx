import React from 'react';
import EditAccountPreference from './EditAccountPreference';

function EditProfilePopUp(props) {

    return (
    <div>
        <div className='popup-background'>
            <EditAccountPreference 
                header="Edit Intro" 
                sx={{marginTop: '100px'}} 
                navigateTo={props.onNavigateBack}/>
        </div>
    </div>
    );
}

export default EditProfilePopUp;

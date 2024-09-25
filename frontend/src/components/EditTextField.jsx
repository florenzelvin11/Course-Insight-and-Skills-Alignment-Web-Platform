import * as React from 'react';
import TextField from '@mui/material/TextField';

function EditTextField (props) {
    return (
    <>
        <TextField 
            multiline={props.multiline}
            type={props.type}
            onChange={props.onChange}
            name={props.name} 
            rows={props.rows}
            label={props.label} 
            value={props.value}
            helperText={props.helperText}
            variant="outlined" 
            fullWidth sx={
                { 
                    mt: 1, 
                    mb: 1,
                    width: '80%',
                    bgcolor: 'white',
                    ...props.sx
                }
            } 
            required={!props.notRequired}
            InputProps={{
                readOnly: props?.readOnly ? true : false,
            }}
        />
    </>
    );
}

export default EditTextField;
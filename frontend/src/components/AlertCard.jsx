import React from 'react'
import Alert from '@mui/material/Alert';

export default function AlertCard(props) {
    return (
        <div className="error-card">
            {props.message && <Alert sx={{ width: '100%', mb: 1}} severity={props.severity}>{props.message}</Alert>}
        </div>
    );
}
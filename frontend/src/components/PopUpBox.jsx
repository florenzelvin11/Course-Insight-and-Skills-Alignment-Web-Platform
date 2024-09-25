import React from 'react'
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { Box } from '@mui/material';

export default function PopUpBox(props) {

    return (
        <>
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
            >{props.title}</DialogTitle>
            <DialogContent 
                dividers={true} 
                sx={{
                    backgroundColor: '#FAFAF5',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                {props.content}
            </DialogContent>
            <Box bgcolor={"#f2f2e4"}>
                <DialogActions>
                        {props.actions}
                </DialogActions>
            </Box>
        </Dialog>
        </>
    )
}
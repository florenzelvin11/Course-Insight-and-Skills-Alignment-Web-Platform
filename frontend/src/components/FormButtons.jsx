import React from 'react'
import { Box, Button } from '@mui/material';

export default function FormButtons(props) {
    return (
        <Box sx={{
            position: 'relative',
            height: '80px',
            width: '80%',
        }}>
            <Box sx={{
                position: 'absolute',
                right: '0px',
            }}>
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    sx={{
                        backgroundColor: '#426B1F', // Set the normal color
                        '&:hover': {
                            backgroundColor: '#274011', // Set the hover color
                        },
                        mb: 5,
                        mt: 1,
                        mr: 1
                    }}
                >
                Save
                </Button>
                {
                    props.cancel
                    &&
                    <>
                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                backgroundColor: '#426B1F', // Set the normal color
                                '&:hover': {
                                    backgroundColor: '#274011', // Set the hover color
                                },
                                mb: 5,
                                mt: 1,
                            }}
                            onClick={props.onCancel}
                        >
                        Cancel
                        </Button>
                    </>
                }
            </Box>
        </Box>
    )
}
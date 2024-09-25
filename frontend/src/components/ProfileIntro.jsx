import React from 'react'
import { Button, Grid, Paper, Box, IconButton, Typography, Avatar } from "@mui/material"
import EditIcon from "@mui/icons-material/Edit"

function AvatarAndBackground() {
    return (
        <Box
            sx={{
                backgroundColor: '#494b4d',
                height: 150,
                width: '100%',
                position: 'relative',
                display: 'flex',
                justifyContent: 'center',
                boxShadow: '0px 12px 20px 0px rgba(0, 0, 0, .2)',
            }}
        >
            <Avatar 
                src=""
                alt=""
                sx={{
                    width: 120,
                    height: 120,
                    zIndex: 1,
                    position: 'absolute',
                    top: '60%'
                }}
            />
        </Box>
    )
}

function NameAndSummary({profileData}) {
    return (
        <Box
            sx={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                position: 'relative', 
                marginTop: 6
            }}
        >
            <Typography variant="h5" component="h2" marginTop={2} fontWeight={600}>{`${profileData.firstName} ${profileData.lastName}`}</Typography>
            <Typography variant="subtitle1" component="subtitle1">{profileData.headline}</Typography>
            <Box sx={{
                marginTop: 1, 
                maxWidth: '300px',
            }}>
                <Typography variant="body2" component="body2">{profileData.summary}</Typography>
            </Box>
        </Box>
    )
}

function NavigateToEdit({onNavigate}) {
    return (
        <IconButton
            color="primary"
            aria-label="Edit Profile"
            component="span"
            sx={{ position: 'absolute', top: '8px', right: '8px', color: 'white'}}
            onClick={onNavigate}
        >
            <EditIcon />
        </IconButton>
    )
}

function AddButton(props) {
    return (
        <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{
                backgroundColor: '#426B1F', // Set the normal color
                '&:hover': {
                    backgroundColor: '#274011', // Set the hover color
                },
                margin: 1, 
                padding: 1.5,
                fontSize: '0.75rem',
                fontWeight: 600,
                lineHeight: '1rem',
                borderRadius: '15px'
            }}
        >
        {props.label}
        </Button>
    )
}

function ProfileIntro({profileData, onNavigateToEditProfile}) {
    return (
        <Grid item xs={12}>
            <Paper 
                sx={{
                    paddingBottom: '10px',
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    position: 'relative',
                    minWidth: '250px',
                    backgroundColor: '#FAFAF5'
                }}
                elevation={3}
                >
                {/* Profile Photo and Background */}
                <AvatarAndBackground />

                {/* Profile Name and Position */}
                <NameAndSummary profileData={profileData} />

                {/* Edit Button */}
                <NavigateToEdit onNavigate={onNavigateToEditProfile} />

                <Box
                    sx={{
                        width: '95%',
                        display: 'flex',
                        justifyContent: 'center',
                        mt: 2,
                    }}
                >
                    {/* Add Course */}
                    <AddButton label="Add Courses"/>
                    {/* Add Projects */}
                    <AddButton label="Add Project"/>
                    {/* Add Skills */}
                    <AddButton label="Add Skills"/>
                </Box>
            </Paper>
        </Grid>
    )
}

export default ProfileIntro;
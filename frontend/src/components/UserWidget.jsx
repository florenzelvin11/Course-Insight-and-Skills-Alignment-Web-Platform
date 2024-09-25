import React from 'react'
import {
    ManageAccountsOutlined,
    SchoolOutlined
} from "@mui/icons-material";
import ShareIcon from '@mui/icons-material/Share';
import { Box, Typography, Divider, IconButton } from "@mui/material";
import UserImage from "./UserImage";
import FlexBetween from "./FlexBetween";
import WidgetWrapper from "./WidgetWrapper";

const UserWidget = (props) => {
    const { userType, profileData } = props
    const {
        zID,
        firstName,
        lastName, 
        headline,
        summary,
        imageURL,
    } = profileData;

    const linkToCopy = `http://localhost:3000/profile/${userType}/${zID}`;

    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(linkToCopy);
            alert('Link copied to clipboard!');
        } catch (error) {
            console.error('Failed to copy:', error);
        }
    }

    return (
        <>
        <WidgetWrapper>
            {/* First Row */}
            <FlexBetween
                gap="0.5rem"
                pb="0.5rem"
            >
                <FlexBetween gap="1rem">
                    <UserImage image={imageURL} />
                    <Box>
                        <Typography 
                            variant="h5"
                            component="h2"
                            color={"black"}
                            fontSize={20}
                            fontWeight="600"
                        >
                            {firstName} {lastName}
                        </Typography>
                    </Box>
                </FlexBetween>

                <FlexBetween>
                    {
                        userType !== 'admin'
                        &&
                        <IconButton
                            color="primary"
                            aria-label="Edit Profile"
                            component="span"
                            // onClick={onNavigate}
                            onClick={copyToClipboard}
                        >
                            <ShareIcon />
                        </IconButton>
                    }

                    {
                        !props?.public
                        &&
                        <IconButton
                            color="primary"
                            aria-label="Edit Profile"
                            component="span"
                            // onClick={onNavigate}
                            onClick={props.handleClickOpen}
                        >
                            <ManageAccountsOutlined />
                        </IconButton>
                    }
                </FlexBetween>
            </FlexBetween>

            {/* Second Row */}
            {
                headline 
                &&
                <>
                <Divider />
                <Box p="1rem 0">
                    <Box display="flex" alignItems="center" gap="1rem" mb="0.5rem">
                        <SchoolOutlined fontSize="large"/>
                        <Typography
                            variant="subtitle1"
                            component="subtitle1"
                        >
                        {headline}
                        </Typography>
                    </Box>
                </Box>
                </>
            }


            {/* Third Row */}
            {
                summary
                &&
                <>
                <Divider />
                <Box p="1rem 0">
                    <Typography fontSize="1rem" fontWeight="600" mb="1rem">
                    About Me
                    </Typography>
                    <Box display="flex" alignItems="center" gap="1rem" mb="0.5rem">
                        <Typography
                            variant="body2"
                            component="body2"
                        >
                        {summary}
                        </Typography>
                    </Box>
                </Box>
                </>
            }
            
        </WidgetWrapper>
        </>
    )

}

export default UserWidget;
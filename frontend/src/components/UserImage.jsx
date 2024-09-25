import React from 'react';
import { Box, Avatar } from '@mui/material';

const UserImage = ({ image, size = "60px"}) => {
    return (
        <Box width={size} height={size}>
            <Avatar 
                src={image || ''}
                alt='user'
                sx={{
                    width: size,
                    height: size,
                    objectFit: "cover", 
                    borderRadius: "50%"
                }}
            />
        </Box>
    )
}

export default UserImage;
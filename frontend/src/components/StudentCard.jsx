import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useNavigate } from 'react-router-dom';
import { Box, Divider } from '@mui/material';
import UserImage from './UserImage';

function StudentCard(props) {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(props.path);
    };

    const {
        firstName,
        lastName,
        headline,
        skills,
        knowledge,
        imageURL
    } = props.profileData

    return (
    <Box>
        <Card 
            onClick={handleClick}
            variant="outlined"
            sx={{ 
                backgroundColor: "#FAFAF5",
                borderRadius: '12px',
                '&:hover': {
                    cursor: 'pointer',
                    backgroundColor: '#dcdcdc',
                    borderRadius: '0px',
                },
                ...props.sx
            }}
        >
            
        <CardContent 
        >
            <Box
                display="flex"
                alignItems="center"
                gap="0.5rem"
            >
                <UserImage image={imageURL} />
                <Box>
                    <Typography gutterBottom variant="h6" component="div" sx={{fontWeight: 600, mb: 0}}>
                        {firstName} {lastName}
                    </Typography>
                    <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600, mt: "0"}}>
                        {headline}
                    </Typography>
                </Box>
            </Box>
            
            <Box m="0.5rem 0">
                <Divider />
            </Box>
            
            <Typography variant="subtitle2" color="text.secondary">
                <strong>Skills:</strong> {skills.slice(0,3).join(', ')}
            </Typography>
            <Typography variant="subtitle2" color="text.secondary">
                <strong>Knowledge Base:</strong> {knowledge.slice(0,3).join(', ')}
            </Typography> 
        </CardContent>
        </Card>
    </Box>
    );
}

export default StudentCard;
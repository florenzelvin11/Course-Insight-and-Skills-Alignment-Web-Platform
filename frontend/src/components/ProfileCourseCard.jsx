import * as React from 'react';
import MediaCard from './MediaCard';
import placeHolderCourseThumbnail from '../assets/placeHolderCourseImage.jpg';
import { Box, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { getUserData } from '../helpers/helper';

function ProfileCourseCard(props) {
    const { courseInfo } = props
    
    const [isHovered, setIsHovered] = React.useState(false);

    return (
        <Box 
            position="relative"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <MediaCard 
                heading={courseInfo.courseName}
                subHeading={courseInfo.courseCode}
                school={courseInfo.school}
                thumbnail={courseInfo.thumbnail || placeHolderCourseThumbnail}
                path={`/course/${courseInfo.courseCode}/${courseInfo.yearDate}-${courseInfo.term}`}
                sx={{...props.sx}}
            />
            {
                ((!props.public || getUserData()?.userType === "admin") && isHovered)
                &&
                <Box
                    sx={{
                        position: 'absolute',
                        top: 0,
                        right: 0,
                    }}
                >
                    <IconButton
                        color="primary"
                        aria-label="Add Courses"
                        component="span"
                        onClick={props.onDelete}
                    >
                        <DeleteIcon sx={{ color: '#f52020' }} fontSize='large'/>
                    </IconButton>  
                </Box>
            }
        </Box>
    );
}

export default ProfileCourseCard;
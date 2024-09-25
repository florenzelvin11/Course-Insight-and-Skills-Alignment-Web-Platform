import React from 'react';
import { Box, List, Paper, Button } from '@mui/material';
import PageHeading from './PageHeading';
import WidgetWrapper from './WidgetWrapper';
import DataTable from './DataTable';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import { useGlobalState } from './GlobalReloadProvider';
import PopUpBox from './PopUpBox';
import NavButton from './NavButton';
import LoadingWidget from './LoadingWidget';
import { apiCall } from '../helpers/helper';

export default function AdminCourses() {

    const headCells = [
        {
            id: 'courseCode',
            label: 'Course Code',
        },
        {
            id: 'courseName',
            label: 'Course Name',
        },
        {
            id: 'yearDate',
            label: 'Year Date',
        },
        {
            id: 'term',
            label: 'Term',
        },
        {
            id: 'school',
            label: 'School',
        },
    ];

    function createData(id, courseCode, courseName, yearDate, term, school) {
        return {
            id,
            courseCode,
            courseName,
            yearDate,
            term,
            school,
        };
    }

    // Data
    const [ data, setData ] = React.useState([]);
    const [ filteredData, setFilteredData ] = React.useState(null);

    const { globalReload, setGlobalReload } = useGlobalState();
    const [ isLoading, setIsLoading ] = React.useState(true)
    const [ openEdit, setOpenEdit ] = React.useState(false);
    const [ openDelete, setOpenDelete ] = React.useState(false);
    const [ course, setCourse ] = React.useState(false);
    const [ selectedCourses, setSelectedCourses ] = React.useState(null)


    React.useEffect(() => {
        async function getCourses() {
            try {
                const response = await apiCall('GET', '/admin/all-courses');
                if (!response.error) {
                    setData(response?.courses.map((item, index) => {
                        const { courseCode, courseName, yearDate, term, school } = item;
                        return createData(index, courseCode, courseName, yearDate, term, school);
                        })
                    )
                    setIsLoading(false);
                }
                return response
            } catch(e) {
                //
                console.log(e.message)
            }
        }
        getCourses()
    }, [openEdit, globalReload])

    function onSelectedCourse(index) {
        console.log(data[index])
        setOpenEdit(true);
        setCourse(data[index])
    }
    
    function handleCancel() {
        setOpenEdit(false)
        setOpenDelete(false)
    }
    
    function handleDelete(selectedCourses) {
        setOpenDelete(true)
        setSelectedCourses(selectedCourses)
    }

    const onDelete = async (coursesId) => {
        try {
            const responses = await Promise.all(coursesId.map((id) => {
                const course = data[id]
                const requestData = { 
                    courseCode: course.courseCode,  
                    yearDate: course.yearDate,
                    term: course.term,
                }
                return apiCall('DELETE', '/admin/course/delete', requestData);
            }));
    
            // Check for errors in the responses
            const hasError = responses.some(response => response.error);
    
            if (!hasError) {
                const updatedData = data.filter(course => !coursesId.includes(course.id))
                setData(updatedData)
                setIsLoading(false)
                setGlobalReload(!globalReload)
            } else {
                console.log('At least one delete operation failed.');
            }
    
        } catch (error) {
            console.log(error.message);
        }
    };

    function onHandleDelete() {
        onDelete(selectedCourses)
        setIsLoading(true)
        setOpenDelete(false)
        console.log(selectedCourses)
    }

    function handleSearchFilter(data, searchItem) {
        return data.filter(course => course.courseName.toLowerCase().includes(searchItem.toLowerCase()));
    }

    const onHandleSearch = async (searchItem) => {
        if (searchItem !== '') {
            setFilteredData(handleSearchFilter(data, searchItem));
        } else {
            setFilteredData(null)
        }
    }

    return (
        <>
        <PageHeading
            title="Active Courses"
        />
        <Box className="container">
            {
                isLoading
                ?
                <LoadingWidget />
                :
                <WidgetWrapper width="95%">
                    <Box>
                        <DataTable 
                            heading={headCells} 
                            data={filteredData !== null? filteredData : data}
                            onSelectedRow={onSelectedCourse}
                            onDelete={handleDelete}
                            onSearchFilter={handleSearchFilter} 
                            onHandleSearch={onHandleSearch}
                        />
                    </Box>
                </WidgetWrapper>
            }
        </Box>
        {
            course !== null
            &&
            <PopUpBox 
                open={openEdit} 
                title={course.courseName}
                content={
                    <>
                    <Paper elevation={3}>
                        <List>
                            <NavButton path={`/course-edit/${course.courseCode}`} label="Edit Course Page" key="editCoursePage" icon={<LibraryBooksIcon />} newTab/>
                        </List>
                    </Paper>
                    </>
                }
                actions={
                <   Button onClick={handleCancel}>Close</Button>
                }
            />
        }

        {/* Delete Prompt Pop Box */}
        <PopUpBox 
            open={openDelete} 
            title={'Delete'}
            content={
                <>
                Are you sure?
                </>
            }
            actions={
            <>
            <Button onClick={handleCancel}>Cancel</Button>
            <Button onClick={onHandleDelete}>Delete</Button>
            </>
            }
        />
        </>
    )
}
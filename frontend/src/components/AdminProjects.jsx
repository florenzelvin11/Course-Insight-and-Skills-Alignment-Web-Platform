import React from 'react';
import { Box, List, Paper, Button } from '@mui/material';
import PageHeading from './PageHeading';
import WidgetWrapper from './WidgetWrapper';
import DataTable from './DataTable';
import { useGlobalState } from './GlobalReloadProvider';
import PopUpBox from './PopUpBox';
import NavButton from './NavButton';
import LoadingWidget from './LoadingWidget';
import { apiCall } from '../helpers/helper';
import DescriptionIcon from '@mui/icons-material/Description';


export default function AdminProjects() {

    const headCells = [
        {
            id: 'projectID',
            label: 'Project ID',
        },
        {
            id: 'projectName',
            label: 'Project Name',
        },
        {
            id: 'client',
            label: 'Client',
        },
    ];

    function createData(id, projectID, projectName, client) {
        return {
            id,
            projectID,
            projectName,
            client,
        };
    }

    // Rows will be passed on my props.data in a json format
    const [ data, setData ] = React.useState([]);
    const [ filteredData, setFilteredData ] = React.useState(null);

    const { globalReload, setGlobalReload } = useGlobalState();
    const [ isLoading, setIsLoading ] = React.useState(true)
    const [ openEdit, setOpenEdit ] = React.useState(false);
    const [ openDelete, setOpenDelete ] = React.useState(false);
    const [ project, setProject ] = React.useState(false);
    const [ selectedProjects, setSelectedProjects ] = React.useState(null)

    React.useEffect(() => {
        async function getProjects() {
            try {
                const response = await apiCall('GET', '/admin/all-projects');

                if (!response.error) {
                    setData(response?.projects.map((item, index) => {
                        const { id, projectName, client } = item;
                        return createData(index, id, projectName, client);
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
        getProjects()
    }, [openEdit, globalReload])

    function onSelectedProject(index) {
        console.log(data[index])
        setOpenEdit(true);
        setProject(data[index])
    }
    
    function handleCancel() {
        setOpenEdit(false)
        setOpenDelete(false)
    }
    
    function handleDelete(selectedProjects) {
        setOpenDelete(true)
        setSelectedProjects(selectedProjects)
    }

    const onDelete = async (projectIds) => {
        try {
            const responses = await Promise.all(projectIds.map((id) => {
                const project = data[id]
                const requestData = { 
                    ID: project.projectID
                }
                return apiCall('DELETE', '/admin/project/delete', requestData);
            }));
    
            // Check for errors in the responses
            const hasError = responses.some(response => response.error);
    
            if (!hasError) {
                const updatedData = data.filter(project => !projectIds.includes(project.id))
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
        onDelete(selectedProjects)
        setIsLoading(true)
        setOpenDelete(false)
    }

    function handleSearchFilter(data, searchItem) {
        return data.filter(project => project.projectName.toLowerCase().includes(searchItem.toLowerCase()));
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
            title="Active Projects"
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
                            onSelectedRow={onSelectedProject}
                            onDelete={handleDelete}
                            onSearchFilter={handleSearchFilter} 
                            onHandleSearch={onHandleSearch}
                        />
                    </Box>
                </WidgetWrapper>
            }
        </Box>
        {
            project !== null
            &&
            <PopUpBox 
                open={openEdit} 
                title={project.projectName}
                content={
                    <>
                    <Paper elevation={3}>
                        <List>
                            <NavButton path={`/project/${project.projectID}`} label="View Project Page" key="viewProjectPage" icon={<DescriptionIcon />} newTab/>
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
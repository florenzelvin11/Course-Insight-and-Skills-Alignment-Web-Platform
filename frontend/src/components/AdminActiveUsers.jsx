import React from 'react';
import { Box, List, Paper } from '@mui/material';
import PageHeading from './PageHeading';
import WidgetWrapper from './WidgetWrapper';
import DataTable from './DataTable';
import PopUpBox from './PopUpBox';
import Button from '@mui/material/Button';
import NavButton from './NavButton';
import PersonIcon from '@mui/icons-material/Person';
import SchoolIcon from '@mui/icons-material/School';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import LoadingWidget from './LoadingWidget';
import { useGlobalState } from './GlobalReloadProvider';
import { apiCall } from '../helpers/helper';

export default function AdminActiveUsers() {

    const headCells = [
        {
            id: 'zID',
            label: 'zID',
        },
        {
            id: 'displayName',
            label: 'Display Name',
        },
        {
            id: 'email',
            label: 'email',
        },
        {
            id: 'userTypes',
            label: 'User Types',
        },
    ];

    function createData(id, zID, displayName, email, userTypes) {
        return {
            id,
            zID,
            displayName,
            email,
            userTypes: userTypes.join(', '),
        };
    }
    
    // Rows will be passed on my props.data in a json format
    const [ data, setData ] = React.useState([]);
    const [ filteredData, setFilteredData ] = React.useState(null);

    const { globalReload, setGlobalReload } = useGlobalState();
    const [ isLoading, setIsLoading ] = React.useState(true)
    const [ openEdit, setOpenEdit ] = React.useState(false);
    const [ openDelete, setOpenDelete ] = React.useState(false);
    const [ user, setUser ] = React.useState(null);
    const [ selectedUsers, setSelectedUsers ] = React.useState(null)


    React.useEffect(() => {
        async function getUsers() {
            try {
                const response = await apiCall('GET', '/admin/all-users');
                
                if (!response.error) {
                    setData(response?.users.map((item, index) => {
                        const { zID, firstName, lastName, email, userType } = item;
                        const displayName = firstName + ' ' + lastName;
                        return createData(index, zID, displayName, email, userType);
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
        getUsers()
    }, [ globalReload ])

    function onSelectedUser(index) {
        console.log(data[index])
        setOpenEdit(true);
        setUser(data[index])
    }
    
    function handleCancel() {
        setOpenEdit(false)
        setOpenDelete(false)
    }
    
    function handleDelete(selectedUsers) {
        setOpenDelete(true)
        setSelectedUsers(selectedUsers)
    }

    const onDelete = async (users) => {
        try {
            const responses = await Promise.all(users.map((user) => {
                const requestData = { zID: data[user].zID }
                return apiCall('DELETE', '/admin/user/delete', requestData);
                // return {requestData}
            }));
    
            // Check for errors in the responses
            const hasError = responses.some(response => response.error);
    
            if (!hasError) {
                const updatedData = data.filter(user => !users.includes(user.id))
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
        onDelete(selectedUsers)
        setIsLoading(true)
        setOpenDelete(false)
        console.log(selectedUsers)
    }

    function handleSearchFilter(data, searchItem) {
        return data.filter(user => user.displayName.toLowerCase().includes(searchItem.toLowerCase()));
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
            title="Active Users"
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
                            onSelectedRow={onSelectedUser} 
                            onDelete={handleDelete} 
                            onSearchFilter={handleSearchFilter} 
                            onHandleSearch={onHandleSearch} />
                    </Box>
                </WidgetWrapper>
            }
            
        </Box>
        {
            user !== null
            &&
            // Edit Pop Box
            <PopUpBox 
                open={openEdit} 
                title={user.displayName}
                content={
                    <>
                    <Paper elevation={3}>
                        <List>
                            <NavButton path={`/profile/student/${user.zID}`} label="Edit Student Page" key="editStudentPage" icon={<PersonIcon />}/>
                            {user.userTypes.includes('academic') && <NavButton path={`/profile/academic/${user.zID}`} label="Edit Academic Page" key="editAcademicPage" icon={<SchoolIcon />}/>}
                            <NavButton path={`/admin/profile/sign-in-and-security/${user.zID}`} label="Edit Sign In & Security" key="editSignInSecurity" icon={<AdminPanelSettingsIcon />}/>
                        </List>
                    </Paper>
                    </>
                }
                actions={
                <   Button onClick={handleCancel}>Cancel</Button>
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
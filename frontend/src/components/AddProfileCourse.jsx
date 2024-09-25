import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import EditTextField from './EditTextField';
import { apiCall } from '../helpers/helper';
import AlertCard from './AlertCard';
import { Box, Typography } from '@mui/material';
import FileUploadForm from './FileUploadForm';
import { useGlobalState } from './GlobalReloadProvider';

export default function AddProfileCourse(props) {
    const { globalReload, setGlobalReload } = useGlobalState()
        
    const [courseData, setCourseData] = React.useState({
        courseCode: null,
        yearDate: null,
        term: null,
    })
    
    const [jsonFile, setJsonFile] = React.useState(null)

    const [selectedFile, setSelectedFile] = React.useState(null);

    const [alert, setAlert] = React.useState({
        severity: null,
        message: null,
    });

    const resetForm = () => {
        setCourseData({
            courseCode: null,
            yearDate: null,
            term: null,
        })
        setSelectedFile(null)
        setJsonFile(null)
    }
    
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setSelectedFile(file);
        if (file) {
            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                setJsonFile(reader.result)
                setGlobalReload(!globalReload);
                setSuccessAlert("Ready to Submit");
            };
        } else {
            setJsonFile(null)
            setErrorAlert("No File Selected");
        }
        setGlobalReload(!globalReload);
    };
        
    function setErrorAlert(message) {
        setAlert({severity : "error", message : message})
    }

    function setSuccessAlert(message) {
        setAlert({severity : "success", message : message})
    }

    function resetAlert() {
        setAlert({severity : null, message : null})
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setCourseData({...courseData, [name]: value }); 
    };
    
    const onSubmit = async () => {
        const requestData = {
            zID: props.zID,
            ...courseData
        }

        const response = await apiCall('POST', `/${props.userType}/course/add`, requestData)
        // const response = {} // Test Successful Post

        if (!response.error) {
            // Make sure courseData is in the right format and then push it into courseCodes.
            setSuccessAlert("Submit Successful!")
            resetAlert()
            resetForm()
            setGlobalReload()
            props.handleSubmit()
        } else {
            setErrorAlert(response.error)
            // setGlobalReload(!globalReload)
        }
        return response
    }

    const onFileSubmit = async () => {
        const requestData = {
            zID: props.zID,
            transcript: jsonFile,
        }

        const response = await apiCall('POST', `/user/profile/${props.userType}/transcript`, requestData)
        // const response = {} // Test Successful Post

        if (!response.error) {
            // Make sure courseData is in the right format and then push it into courseCodes.
            setSuccessAlert("Submit Successful!")
            resetAlert()
            resetForm()
            setGlobalReload()
            props.handleSubmit()
        } else {
            // setErrorAlert("Try Again")
            setErrorAlert(response.error)
        }
        return response
    }

    const checkIsNumber = (inputValue) => {
        if (inputValue === null) return false;
        return !isNaN(inputValue) ? true : false
    };

    const checkIsTerm = (inputValue) => {
        return (inputValue === "T1") || (inputValue === "T2") || (inputValue === "T3")
    }

    const handleSubmit = (e) => {
        e.preventDefault()

        if (selectedFile !== null && jsonFile !== null) {
            onFileSubmit()
        } else {
            if (!courseData.courseCode) {
                setErrorAlert("Please enter a Course Code or a File")
                return;
            } else if (!checkIsNumber(courseData.yearDate)) {
                setErrorAlert("Please enter a valid Year")
                return;
            } else if (!checkIsTerm(courseData.term)) {
                setErrorAlert("Please enter a valid Term")
                return;
            }
            onSubmit()    
        }
    };

    const handleCancel = (e) => {
        e.preventDefault()
        props.handleClose()
        resetAlert()
        resetForm()
    }

  return (
    <div>
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
        >
            Add Course
        </DialogTitle>
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
            <EditTextField onChange={handleInputChange} name="courseCode" label="Course Code" value={courseData.courseCode} notRequired />
            
            <Box display={'flex'} alignItems={'center'} gap={0.5} width="80%">
                <EditTextField onChange={handleInputChange} name="yearDate" label="Year" value={courseData.yearDate} notRequired />
                <EditTextField onChange={handleInputChange} name="term" label="Term" value={courseData.term} notRequired />
            </Box>

            {
                props.userType === 'student'
                &&
                <>
                <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600, mt: "0"}}>
                    <Box display={'flex'} alignItems={'center'}>
                        <div className="vertical-line"></div>
                        or 
                        <div className="vertical-line"></div>
                    </Box>
                </Typography>
                
                <FileUploadForm handleFileChange={handleFileChange} selectedFile={selectedFile}/>
                </>
            }
            <AlertCard severity={alert.severity} message={alert.message} />
        </DialogContent>
        <Box bgcolor={"#f2f2e4"}>
            <DialogActions>
                <Button onClick={handleCancel}>Cancel</Button>
                <Button onClick={handleSubmit}>Submit</Button>
            </DialogActions>
        </Box>
      </Dialog>
    </div>
  );
}

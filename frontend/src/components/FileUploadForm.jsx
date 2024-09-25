import React from 'react';
import { Button, TextField } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function FileUploadForm(props) {

  return (
  <div style={{ 
      width: "80%",
      display: "flex", 
      justifyContent: "center", 
      alignItems: "center"
    }}  
  >
    <input
      type="file"
      id="fileInput"
      accept=".pdf, .doc, .docx" // Specify accepted file types
      style={{ display: 'none' }}
      onChange={props.handleFileChange}
    />
    <TextField
      label="Select a File"
      value={props.selectedFile ? props.selectedFile.name : ''}
      fullWidth
      InputProps={{
        readOnly: true,
      }}
      variant="outlined"
      sx={{
          bgcolor: "white",
          m: "1rem 0",
          pr: "0.5rem"
      }}
    />

    <label htmlFor="fileInput">
        <Button
          variant="contained"
          color="primary"
          component="span"
          startIcon={<CloudUploadIcon />}
        >
          Upload File
        </Button>
      </label>
    </div>
  );
}

export default FileUploadForm;

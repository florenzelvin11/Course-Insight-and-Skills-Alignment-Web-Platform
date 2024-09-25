import * as React from "react";
import { useState } from "react";
import { Button, Box, Typography } from "@mui/material";

function PdfUploader(props) {
  const [file, setFile] = useState(null);

  const handleUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = () => {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      let dataURL = reader.result;
      props.onSubmit(dataURL);
    };
  };

  return (
    <>
      <Box>
        <div className="add-button-container">
          <input
            accept="application/pdf"
            style={{ display: "none" }}
            id="upload-button"
            type="file"
            onChange={handleUpload}
          />
          <label htmlFor="upload-button">
            <Button
              sx={{
                color: "white",
                backgroundColor: "#426B1F",
                "&:hover": {
                  backgroundColor: "#274011",
                },
                width: "100%",
                mb: 2,
                mt: 1,
              }}
              label="Upload"
              component="span"
            >
              Choose file
            </Button>
          </label>
        </div>
        {file && (
          <div className="add-button-container">
            <Typography sx={{ textAlign: "center" }} variant="h9">
              Uploaded file: {file.name}
            </Typography>
            <Button
              onClick={handleSubmit}
              sx={{
                color: "white",
                backgroundColor: "#426B1F",
                "&:hover": {
                  backgroundColor: "#274011",
                },
                width: "80%",
                mb: 5,
                mt: 1,
              }}
              label="Upload"
              component="span"
            >
              Upload file
            </Button>
          </div>
        )}
      </Box>
    </>
  );
}

export default PdfUploader;

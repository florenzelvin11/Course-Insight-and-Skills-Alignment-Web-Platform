import * as React from "react";
import Button from "@mui/material/Button";

function SubmitButton(props) {
  const buttonText = props.label;
  return (
    <>
      <Button
        onClick={props.onClick}
        id={props.id}
        variant="contained"
        color="secondary"
        sx={{
          backgroundColor: "#426B1F",
          "&:hover": {
            backgroundColor: "#274011",
          },
          width: "80%",
          mb: 5,
          mt: 1,
        }}
        fullWidth
      >
        {buttonText}
      </Button>
    </>
  );
}

export default SubmitButton;

import * as React from "react";
import { useState } from "react";
import { Button, Modal } from "@mui/material";
import EditTextField from "./EditTextField";

function FormModal(props) {
  const [input, setInput] = useState("");

  const inputChange = (event) => {
    const { value } = event.target;
    setInput(value);
  };

  function handleClose() {
    props.handleClose(input);
  }

  return (
    <Modal open={props.open} onClose={handleClose}>
      <div className="succuess-modal-container">
        <div className="succuess-modal">
          <h1 className="succuess-modal-text">{props.heading}</h1>
          <EditTextField
            value={input}
            onChange={inputChange}
            label="Group Name"
          />
          <Button
            onClick={handleClose}
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
          >
            {props.buttonText}{" "}
          </Button>
        </div>
      </div>
    </Modal>
  );
}

export default FormModal;

import * as React from "react";
import { Button, Modal } from "@mui/material";

function ResultModal(props) {
  return (
    <Modal open={props.open} onClose={props.handleClose}>
      <div className="succuess-modal-container">
        <div className="succuess-modal">
          <h1 className="succuess-modal-text">{props.heading}</h1>
          <Button
            onClick={props.handleClose}
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

export default ResultModal;

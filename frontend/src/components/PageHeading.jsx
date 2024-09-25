import * as React from "react";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AddIcon from "@mui/icons-material/Add";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

function PageHeading(props) {
  const navigate = useNavigate();

  function navigateBack() {
    navigate(props.backPath);
  }

  function handleAction() {
    navigate(props.actionPath);
  }

  return (
    <>
      <div className="page-heading">
        {props.backButtonName && props.backPath && (
          <div className="page-heading--back-arrow">
            <Button onClick={navigateBack} sx={{ color: "#426B1F" }}>
              <ArrowBackIcon sx={{ mr: 1 }} />
              {props.backButtonName}
            </Button>
          </div>
        )}
        <div className="page-heading-header">
          <h1 className="page-heading--title">{props.title}</h1>
          {props.actionName && props.actionPath && (
            <Button sx={{ color: "#426B1F" }} onClick={handleAction}>
              {props.actionName}
              <AddIcon />
            </Button>
          )}
        </div>
        <div className="page-heading--divding-line" />
      </div>
    </>
  );
}

export default PageHeading;

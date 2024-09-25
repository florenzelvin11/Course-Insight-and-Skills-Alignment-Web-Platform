import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import { useNavigate } from "react-router-dom";

function AuthNavBar(props) {
  const navigate = useNavigate();

  function buttonClickHandler() {
    if (props.buttonLabel === "sign up") {
      navigate("/signup");
    } else {
      navigate("/");
    }
  }

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" sx={{ backgroundColor: "#426B1F" }}>
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
            ></IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Application Name
            </Typography>
            <Button onClick={buttonClickHandler} color="inherit">
              {props.buttonLabel}
            </Button>
          </Toolbar>
        </AppBar>
      </Box>
    </>
  );
}

export default AuthNavBar;

import * as React from "react";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { useNavigate } from "react-router-dom";
import { logOut } from "../helpers/helper";

function NavButton(props) {
  const navigate = useNavigate();

    function handleClick () {
        if (props.label === 'Logout') {
            logOut();
        }
        if (props.newTab) {
            window.open(props.path, '_blank');
        } else {
            navigate(props.path);
        }
    }

  return (
    <>
      <ListItem disablePadding>
        <ListItemButton onClick={handleClick}>
          <ListItemIcon>{props.icon}</ListItemIcon>
          <ListItemText primary={props.label} />
        </ListItemButton>
      </ListItem>
    </>
  );
}

export default NavButton;

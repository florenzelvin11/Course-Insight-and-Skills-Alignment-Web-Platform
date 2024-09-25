import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

function DropDownInput(props) {
  return (
    <>
      <FormControl
        required
        sx={{
          mt: 1,
          mb: 2,
          width: "80%",
          bgcolor: "white",
        }}
      >
        <InputLabel>{props.label}</InputLabel>
        <Select
          name={props.name}
          label={props.label}
          value={props.selectedOption}
          onChange={props.onChange}
        >
          {props.menuItems.map((menuItem, index) => (
            <MenuItem key={index} value={menuItem.value}>
              {menuItem.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

export default DropDownInput;

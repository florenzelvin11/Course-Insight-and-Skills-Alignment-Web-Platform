import * as React from "react";
import TextField from "@mui/material/TextField";

function AuthTextField(props) {
  return (
    <>
      <TextField
        type={props.type}
        onChange={props.onChange}
        name={props.name}
        label={props.label}
        value={props.value}
        variant="outlined"
        fullWidth
        sx={{
          mt: 1,
          mb: 1,
          width: "80%",
          bgcolor: "white",
          ...props.sx,
        }}
        required
      />
    </>
  );
}

export default AuthTextField;

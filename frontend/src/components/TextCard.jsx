import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import EditCardButton from "./EditCardButton";

function TextCard(props) {
  return (
    <>
      <Card
        variant="outlined"
        sx={{
          mt: 2,
          backgroundColor: "#FAFAF5",
          borderRadius: "12px",
        }}
      >
        <CardContent>
          <Typography variant="h4" component="div">
            {props.heading}
          </Typography>
          <Typography sx={{ mt: 1 }} variant="body1">
            {props.content}
          </Typography>
        </CardContent>
        {props.editPath && <EditCardButton path={props.editPath} />}
      </Card>
    </>
  );
}

export default TextCard;

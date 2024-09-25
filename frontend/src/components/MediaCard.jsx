import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";

function MediaCard(props) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(props.path);
  };

  return (
    <>
      <Card
        onClick={handleClick}
        variant="outlined"
        sx={{
          minWidth: 0,
          width: "100%",
          height: "100%",
          backgroundColor: "#FAFAF5",
          borderRadius: "20px",
          transition: "background-color 0.7s ease, border-radius 0.8s ease",
          "&:hover": {
            cursor: "pointer",
            backgroundColor: "#dcdcdc",
            borderRadius: "3px",
          },
          ...props.sx,
        }}
      >
        <CardMedia sx={{ height: 140 }} image={props.thumbnail} />
        <CardContent>
          <Typography
            gutterBottom
            variant="h6"
            component="div"
            sx={{ fontWeight: 600, mb: 0 }}
          >
            {props.heading}
          </Typography>
          <Typography
            variant="subtitle1"
            color="text.secondary"
            sx={{ color: "#426B1F", fontWeight: 600 }}
          >
            {props.subHeading}
          </Typography>
          <Typography variant="subtitle2" color="text.secondary">
            {props.school}
          </Typography>
        </CardContent>
      </Card>
    </>
  );
}

export default MediaCard;

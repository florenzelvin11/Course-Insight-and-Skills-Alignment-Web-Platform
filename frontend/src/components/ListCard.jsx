import * as React from "react";
import Card from "@mui/material/Card";
import { useState, useEffect } from "react";
import CardContent from "@mui/material/CardContent";
import List from "@mui/material/List";
import Box from "@mui/material/Box";
import ListItemText from "@mui/material/ListItemText";
import ListItem from "@mui/material/ListItem";
import Typography from "@mui/material/Typography";
import EditCardButton from "./EditCardButton";

function ListCard(props) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const getSkills = async () => {
      if (props.items) {
        setItems(props.items);
      }
    };

    getSkills();
  }, [props.items]);

  return (
    <>
      {items.length > 0 && (
        <Card
          variant="outlined"
          sx={{
            mt: 2,
            pb: 0,
            backgroundColor: "#FAFAF5",
            borderRadius: "12px",
          }}
        >
          <CardContent sx={{ pb: 0 }}>
            <Typography variant="h4" component="div">
              {props.heading}
            </Typography>
            <div className="chart-card-container">
              <Box sx={{ pb: 0 }}>
                <List dense={true} sx={{ pb: 0 }}>
                  {items.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemText sx={{ fontSize: "16px" }}>
                        {index + 1}. {item}
                      </ListItemText>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </div>
          </CardContent>
          {props.editPath && <EditCardButton path={props.editPath} />}
        </Card>
      )}
    </>
  );
}

export default ListCard;

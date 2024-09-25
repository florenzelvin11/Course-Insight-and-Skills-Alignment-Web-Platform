import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import List from "@mui/material/List";
import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import ListItemText from "@mui/material/ListItemText";
import ListItem from "@mui/material/ListItem";
import Typography from "@mui/material/Typography";
import SkillsPieChart from "./SkillsPieChart";
import EditCardButton from "./EditCardButton";
import { objectToArray } from "../helpers/helper";

function ChartCard(props) {
  const [skills, setSkills] = useState([]);
  const [sortedSkills, setSortedSkills] = useState([]);

  useEffect(() => {
    const getSkills = async () => {
      if (props.skills) {
        const formattedSkills = objectToArray(props.skills);
        const sortedSkills = formattedSkills.sort(
          (a, b) => parseInt(b.weight) - parseInt(a.weight)
        );
        setSortedSkills(sortedSkills);
        setSkills(formattedSkills);
      }
    };

    getSkills();
  }, [props.skills]);

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
          <div className="chart-card-container">
            <Box>
              <List dense={true}>
                {sortedSkills.map((item, index) => (
                  <ListItem key={index}>
                    <ListItemText sx={{ fontSize: "16px" }}>
                      {index + 1}. {item.name}
                    </ListItemText>
                  </ListItem>
                ))}
              </List>
            </Box>
            <SkillsPieChart skills={skills} />
          </div>
        </CardContent>
        {props.editPath && <EditCardButton path={props.editPath} />}
      </Card>
    </>
  );
}

export default ChartCard;

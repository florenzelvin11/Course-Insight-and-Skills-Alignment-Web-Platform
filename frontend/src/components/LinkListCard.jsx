import * as React from "react";
import Card from "@mui/material/Card";
import { useState, useEffect } from "react";
import CardContent from "@mui/material/CardContent";
import List from "@mui/material/List";
import Box from "@mui/material/Box";
import ListItem from "@mui/material/ListItem";
import Typography from "@mui/material/Typography";
import EditCardButton from "./EditCardButton";
import Link from "@mui/material/Link";
import { Link as RouterLink } from "react-router-dom";
import { canAdd } from "../helpers/helper";
import { Button } from "@mui/material";

function LinkListCard(props) {
  const [item, setItem] = useState("");
  const [members, setMembers] = useState([]);
  const [userInGroup, setUserInGroup] = useState(false);

  useEffect(() => {
    const getSkills = async () => {
      if (props.item) {
        setItem(props.item);
        setMembers(props.item.members);
      }

      if (props.userInGroup) {
        setUserInGroup(props.userInGroup);
      }
    };

    getSkills();
  }, [props.item, props.userInGroup]);

  function handleJoinGroup() {
    props.joinGroup(item.id);
  }
  return (
    <>
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
          <Typography variant="h5" component="div">
            {item.groupName}
          </Typography>
          <div className="chart-card-container">
            <Box sx={{ pb: 0 }}>
              <List dense={true} sx={{ pb: 0 }}>
                {members.map((member, index) => (
                  <ListItem key={index}>
                    <Link
                      sx={{ fontSize: "16px" }}
                      component={RouterLink}
                      to={`/profile/student/${member}`}
                      underline="hover"
                    >
                      {index + 1}. {member}
                    </Link>
                  </ListItem>
                ))}
              </List>
            </Box>
          </div>
          {!canAdd() && !userInGroup && (
            <Button sx={{ mt: 2, color: "#426B1F" }} onClick={handleJoinGroup}>
              Join Group
            </Button>
          )}
        </CardContent>
        {props.editPath && <EditCardButton path={props.editPath} />}
      </Card>
    </>
  );
}

export default LinkListCard;

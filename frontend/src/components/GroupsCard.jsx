import * as React from "react";
import Card from "@mui/material/Card";
import { useState, useEffect } from "react";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import LinkListCard from "./LinkListCard";
import { canAdd } from "../helpers/helper";
import { Button } from "@mui/material";

function GroupsCard(props) {
  const [groups, setGroups] = useState([]);
  const [userInGroup, setUserInGroup] = useState(false);

  useEffect(() => {
    const getGroups = async () => {
      if (props.groups) {
        setGroups(props.groups);
      }

      if (props.userInGroup) {
        setUserInGroup(props.userInGroup);
      }
    };

    getGroups();
  }, [props.groups, props.userInGroup]);

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
          <Typography variant="h4" component="div">
            Groups
          </Typography>

          {groups.map((group, index) => (
            <LinkListCard
              key={index}
              item={group}
              joinGroup={props.joinGroup}
              userInGroup={userInGroup}
            />
          ))}
          {!canAdd() && !userInGroup && (
            <Button
              sx={{ mt: 3, color: "#426B1F" }}
              onClick={props.createGroup}
            >
              Create Group
            </Button>
          )}
        </CardContent>
      </Card>
    </>
  );
}

export default GroupsCard;

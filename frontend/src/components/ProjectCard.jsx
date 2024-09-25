import * as React from "react";
import MediaCard from "./MediaCard";
import placeHolderCourseThumbnail from "../assets/placeHolderCourseImage.jpg";

function ProjectCard(props) {
  return (
    <>
      <MediaCard
        heading={props.name}
        subHeading={props.knowledge.join(", ")}
        school={props.client}
        thumbnail={props.thumbnail || placeHolderCourseThumbnail}
        path={`/project/${props.id}`}
        sx={{ width: "370px" }}
      />
    </>
  );
}

export default ProjectCard;

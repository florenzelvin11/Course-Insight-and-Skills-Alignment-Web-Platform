import * as React from "react";
import MediaCard from "./MediaCard";
import placeHolderCourseThumbnail from "../assets/placeHolderCourseImage.jpg";

function CourseCard(props) {
  return (
    <div>
      <MediaCard
        heading={props.name}
        subHeading={props.code}
        school={props.school}
        thumbnail={props.thumbnail || placeHolderCourseThumbnail}
        path={`/course/${props.code}`}
        sx={{ ...props.sx }}
      />
    </div>
  );
}

export default CourseCard;

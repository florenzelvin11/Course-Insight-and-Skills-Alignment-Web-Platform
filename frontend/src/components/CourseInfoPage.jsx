import * as React from "react";
import TextCard from "./TextCard";
import ChartCard from "./ChartCard";
import ListCard from "./ListCard";

function CourseInfoPage(props) {
  return (
    <>
      <div className="info-container">
        <div className="info-card">
          <div className="info">
            <TextCard
              editPath={props.editPath}
              heading="Description"
              content={props.data.description}
            />
          </div>
          <div className="info">
            <ListCard
              editPath={props.editPath}
              heading="Topics"
              items={props.data.topics}
            />
          </div>
          <div className="info">
            <ChartCard
              editPath={props.editPath}
              heading="Skills"
              skills={props.data.skills}
            />
          </div>
          <div className="info">
            <ChartCard
              editPath={props.editPath}
              heading="Knowledge"
              skills={props.data.knowledge}
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default CourseInfoPage;

import * as React from "react";
import TextCard from "./TextCard";
import ChartCard from "./ChartCard";
import ListCard from "./ListCard";
import GroupsCard from "./GroupsCard";
import { canAdd } from "../helpers/helper";

function ProjectInfoPage(props) {
  return (
    <>
      <div className="info-container">
        <div className="info-card">
          <div className="join-project-button"></div>
          <div className="info">
            <TextCard heading="Scope" content={props.data.scope} />
          </div>
          <div className="info">
            <TextCard heading="Client" content={props.data.client} />
          </div>
          <div className="info">
            <ListCard heading="Topics" items={props.data.topics} />
          </div>
          <div className="info">
            <TextCard heading="Outcomes" content={props.data.outcomes} />
          </div>
          <div className="info">
            <TextCard
              heading="Requirements"
              content={props.data.requirements}
            />
          </div>
          <div className="info">
            <ChartCard
              heading="Knowledge Required"
              skills={props.data.knowledge}
            />
          </div>
          <div className="info">
            <ChartCard heading="Skills Required" skills={props.data.skills} />
          </div>
          <div className="info">
            <GroupsCard
              heading="Groups"
              groups={props.data.groups}
              createGroup={props.createGroup}
              joinGroup={props.joinGroup}
              userInGroup={props.userInGroup}
            />
          </div>
          {!canAdd() && (
            <>
              <h1>Skill Gap Analysis</h1>
              <h2>Percentage Match: {props.data.percentageMatch}%</h2>
              <div className="info">
                <ListCard
                  heading="Missing Skills"
                  items={props.data.missingSkills}
                />
              </div>
              <div className="info">
                <ListCard
                  heading="Missing Knowledge"
                  items={props.data.missingKnowledge}
                />
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}

export default ProjectInfoPage;

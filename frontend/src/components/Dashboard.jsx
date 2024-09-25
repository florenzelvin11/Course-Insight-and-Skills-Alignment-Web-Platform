import * as React from "react";

function Dashboard(props) {
  return (
    <>
      <div className="dashboard-container">
        {props.content}
        {props.error}
      </div>
    </>
  );
}

export default Dashboard;

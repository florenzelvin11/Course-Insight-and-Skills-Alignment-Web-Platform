import * as React from "react";
import { PieChart } from "@mui/x-charts/PieChart";

//  https://mui.com/x/react-charts/pie/
function SkillsPieChart(props) {
  const colours = [
    "#BD94E0",
    "#E094BD",
    "#94E094",
    "#E094E0",
    "#94BDE0",
    "#E0BD94",
    "#5A6B04",
    "#E06B5A",
    "#1F2B0E",
    "#E02B1F",
    "#FFA500",
    "#7C1C1C",
    "#1C7C3E",
    "#1C3E7C",
    "#3E1C7C",
    "#7C3E1C",
    "#4D4D4D",
    "#7C1C5B",
    "#5B7C1C",
    "#1C5B7C",
    "#7C5B1C",
    "#5B1C7C",
    "#FF5733",
    "#33FF57",
    "#5733FF",
    "#FF33E9",
    "#E9FF33",
    "#33E9FF",
    "#FF33A8",
    "#A8FF33"
  ];

  function getData() {
    return props.skills.map((skill, index) => ({
      id: index,
      value: parseInt(skill.weight),
      label: skill.name,
      color: colours[index],
    }));
  }

  return (
    <PieChart
      series={[
        {
          data: getData(),
        },
      ]}
      width={420}
      height={200}
    />
  );
}

export default SkillsPieChart;

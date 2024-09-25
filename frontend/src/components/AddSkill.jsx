import React from "react";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import Button from "@mui/material/Button";
import { useState } from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";
import Tooltip from "@mui/material/Tooltip";

function AddSkill(props) {
  const [skillCount, setSkillCount] = useState(props.skills.length);
  const handleInputChange = (index, event) => {
    const { name, value } = event.target;
    const updatedSkills = [...props.skills];
    let setValue = value;
    if (name === "weight" && value) {
      setValue = parseInt(value);
    }
    updatedSkills[index] = { ...updatedSkills[index], [name]: setValue };
    props.onSkillChange(updatedSkills);
  };

  const handleAddField = () => {
    props.onSkillChange([...props.skills, { name: "", weight: "" }]);
    setSkillCount(props.skills.length);
  };

  const handleRemoveField = (index) => {
    const updatedSkills = props.skills.filter((_, i) => i !== index);
    props.onSkillChange(updatedSkills);
    setSkillCount(props.skills.length);
  };

  const addFieldButton = () => {
    return (
      <>
        {skillCount < 4 && (
          <Button
            sx={{ mb: 3, mt: 4, width: "100%" }}
            fullWidth
            onClick={handleAddField}
            variant="outlined"
            startIcon={<AddIcon />}
          >
            {`Add ${props.label}`}
          </Button>
        )}
      </>
    );
  };

  return (
    <div className="add-skills-container">
      {props.skills.map((skill, index) => (
        <div key={index} className="add-skills">
          <TextField
            sx={{ width: "30%", mr: 2, mt: 3, bgcolor: "white" }}
            name="name"
            label={props.label}
            value={skill.name}
            onChange={(e) => handleInputChange(index, e)}
          />
          <TextField
            sx={{ width: "50%", mr: 2, mt: 3, bgcolor: "white" }}
            name="weight"
            label="Weight"
            type="number"
            InputProps={{
              endAdornment: <InputAdornment position="end">%</InputAdornment>,
              inputMode: "numeric",
              pattern: "[0-9]*",
              maxLength: 3,
            }}
            value={skill.weight}
            onChange={(e) => handleInputChange(index, e)}
          />
          <Button
            sx={{ width: "10%", mt: 4 }}
            onClick={() => handleRemoveField(index)}
            variant="outlined"
          >
            <Tooltip title={`Delete ${skill.name}`}>
              <DeleteIcon />
            </Tooltip>
          </Button>
        </div>
      ))}
      {addFieldButton()}
    </div>
  );
}

export default AddSkill;

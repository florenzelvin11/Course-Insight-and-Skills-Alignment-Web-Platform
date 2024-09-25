import React from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";
import Tooltip from "@mui/material/Tooltip";

function AddTopic(props) {
  const handleInputChange = (index, event) => {
    const { value } = event.target;
    const updatedTopics = [...props.topics];
    updatedTopics[index] = value;
    props.onTopicChange(updatedTopics);
  };

  const handleAddField = () => {
    props.onTopicChange([...props.topics, ""]);
  };

  const handleRemoveField = (index) => {
    const updatedTopics = props.topics.filter((_, i) => i !== index);
    props.onTopicChange(updatedTopics);
  };

  return (
    <div className="add-skills-container">
      {props.topics.map((topic, index) => (
        <div key={index} className="add-topic">
          <TextField
            sx={{ width: "90%", mr: 2, mt: 3, bgcolor: "white" }}
            label={props.label}
            value={topic}
            onChange={(e) => handleInputChange(index, e)}
          />
          <Button
            sx={{ width: "10%", mt: 3 }}
            onClick={() => handleRemoveField(index)}
            variant="outlined"
          >
            <Tooltip title={`Delete Topic`}>
              <DeleteIcon />
            </Tooltip>
          </Button>
        </div>
      ))}
      <Button
        sx={{ mb: 3, mt: 4, width: "100%" }}
        fullWidth
        onClick={handleAddField}
        variant="outlined"
        startIcon={<AddIcon />}
      >
        {`Add ${props.label}`}
      </Button>
    </div>
  );
}

export default AddTopic;

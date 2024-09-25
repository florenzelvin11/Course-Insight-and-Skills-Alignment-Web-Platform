import * as React from "react";
import { useState, useEffect } from "react";
import DropDownInput from "../components/DropDownInput";

function VersionDropDown(props) {
  const [currentVersion, setCurrentVersion] = useState({ version: "" });
  const [versions, setVersions] = useState([]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setCurrentVersion({ ...currentVersion, [name]: value });
    props.onSelection(value);
  };

  useEffect(() => {
    const configureVersions = async () => {
      if (props.versions) {
        const versionList = [];

        for (const version of props.versions) {
          versionList.push({
            label: version,
            value: version,
          });
        }
        setVersions(versionList);
      }
      if (props.currentVersion) {
        setCurrentVersion({ version: props.currentVersion });
      }
    };

    configureVersions();
  }, [props.versions, props.currentVersion]);

  return (
    <>
      <div className="verion-menu-container">
        <div className="verion-menu">
          <DropDownInput
            onChange={handleChange}
            selectedOption={currentVersion.version}
            name="version"
            label={props.label}
            menuItems={versions}
          />
        </div>
      </div>
    </>
  );
}

export default VersionDropDown;

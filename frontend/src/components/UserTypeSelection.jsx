import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import { useState } from 'react';
import FormLabel from '@mui/material/FormLabel';
import { getHighestUserType, getUserType, setUserType } from '../helpers/helper';
import { useGlobalState } from './GlobalReloadProvider';

function UserTypeSelection() {
  const [type, setType] = useState(getUserType());
  const { globalReload, setGlobalReload } = useGlobalState();

  const handleChange = (event) => {
    setType(event.target.value);
    setUserType(event.target.value);
    setGlobalReload(!globalReload);
  };

  return (
    <>
      <div className='user-type-selection'> 
        <FormControl>
          <FormLabel sx={{'&.Mui-focused': { color: '#426B1F' }}}>View As</FormLabel>
          <RadioGroup
            value={type}
            onChange={handleChange}
          >
            <FormControlLabel value="student" control={<Radio sx={{'&.Mui-checked': { color: '#426B1F' }}}/>} label="Student" />
            <FormControlLabel value="academic" control={<Radio sx={{'&.Mui-checked': { color: '#426B1F' }}}/>} label="Academic" />
            {getHighestUserType() === 'admin' && <FormControlLabel value="admin" control={<Radio sx={{'&.Mui-checked': { color: '#426B1F' }}}/>} label="Admin" />}
          </RadioGroup>
        </FormControl>
      </div>
    </>
  );
}

export default UserTypeSelection;

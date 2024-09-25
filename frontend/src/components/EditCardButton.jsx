import * as React from 'react';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import { canAdd } from '../helpers/helper';
import { useNavigate } from 'react-router-dom';


function EditCardButton(props) {
  const navigate = useNavigate();

  function handleEdit() {
    navigate(props.path);
  }

  return (
    <>
      {canAdd() && 
          <CardActions  sx={{ mt: 0 }}>
              <Button onClick={handleEdit} size="small" sx={{ fontSize: '16px', ml: 0, mt: 0, color: "#426B1F"}}>Edit</Button>
          </CardActions>
      }
    </>
  );
}

export default EditCardButton;
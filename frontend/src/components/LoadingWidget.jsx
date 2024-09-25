import React from 'react';
import { CircularProgress, Box } from '@mui/material';

const LoadingWidget = () => {
  return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100%"
      >
        <CircularProgress size={80} style={{ color: '#426B1F' }} />
      </Box>
  );
};

export default LoadingWidget;

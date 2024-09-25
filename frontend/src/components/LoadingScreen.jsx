import React from 'react';
import { CircularProgress } from '@mui/material';
import { styled } from '@mui/material/styles';

const LoadingDiv = styled('div')(() => ({
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    width: '100vw',
}));

const LoadingScreen = () => {

  return (
    <LoadingDiv>
      <CircularProgress size={80} style={{ color: '#426B1F' }} />
    </LoadingDiv>
  );
};

export default LoadingScreen;

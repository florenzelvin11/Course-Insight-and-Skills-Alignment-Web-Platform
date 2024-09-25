import { createTheme } from '@material-ui/core/styles';

// A custom theme for this app
const theme = createTheme({
  palette: {
    primary: {
      main: '#426B1F',
    },
    secondary: {
      main: '#FAFAF5',
    },
    background: {
      default: 'white',
      alt: '#FAFAF5'
    },
  },
  components: {
    MuiInputBase: {
      styleOverrides: {
        // Override styles for autofill
        '& input:-webkit-autofill': {
          transition: 'background-color 5000s ease-in-out 0s', // Delay the transition to override browser styles
        },
        // Override styles for autocomplete placeholder
        '& input::placeholder': {
          color: '#757575',
        },
      },
    },
  },
});

export default theme;
import * as React from 'react';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';

const SearchBar = (props) => {
    const [isFocused, setIsFocused] = React.useState(false);
    const [ value, setValue ] = React.useState('')
    
    const handleSearch = (event) => {
        // handle your search functionality here
        console.log('Search keyword:', event.target.value);
        setValue(event.target.value)
        // You can implement your search logic here using the event.target.value
        // For example, make an API call or filter/search through your data.
    };

    const handleSubmit = (e) => {
        e.preventDefault()
        // handle your search functionality here
        console.log('Submitted keyword:', value);
        // You can implement your search logic here using the event.target.value
        // For example, make an API call or filter/search through your data.
        props.onSearch(value)
    };

  return (
    <form onSubmit={handleSubmit} noValidate autoComplete="off">
      <TextField
        id="search"
        label="Search by Name"
        variant="outlined"
        onChange={handleSearch}
        value={value}
        InputProps={{
          endAdornment: (
            <IconButton type="submit" aria-label="search">
              <SearchIcon />
            </IconButton>
          ),
        }}
        sx={{
            backgroundColor: 'white',
            '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  border: isFocused ? '2px solid #000' : '1px solid #000',
                },
              },
            borderRadius: '5px',
        }}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
    </form>
  );
};

export default SearchBar;

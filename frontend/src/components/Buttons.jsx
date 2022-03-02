import React, { useState } from 'react';
import { styled, StyledEngineProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import './Buttons.css';

const Input = styled('input')({
  display: 'none',
});


export const UploadButton = (props) => {
  const [files, setFiles] = useState([]);

  const handleUpload = (event) => {
    const inputFiles = event.target.files
    // Empty array before adding files
    setFiles([])
    // Add each file to the array
    for (const inputFile of inputFiles) {
      setFiles(arr => [...arr, inputFile])
    }
  }

  return (
    <StyledEngineProvider injectFirst>
      <form>
        <label htmlFor="contained-button-file">
          <Input accept="image/*" id="contained-button-file" multiple type="file" onChange={handleUpload}/>
          <Button component='span' className={props.buttonType + ' button-upload'} variant="contained" size='large'>
            {props.buttonText}
          </Button>
          <p>Antall Filer valgt: {files.length}</p>
        </label>
      </form>
    </StyledEngineProvider >
  );
}
UploadButton.defaultProps = {
  buttonType: "button"
}

export const SubmitButton = () => {
  return (<Button className='button' size="medium" variant="contained">Submit</Button>);
}

export const CancelButton = (props) => {
  return (<Button size="medium" component={props.component} to={props.to}>Cancel</Button>);
}
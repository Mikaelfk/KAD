import * as React from 'react';
import { styled, StyledEngineProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import './Buttons.css';

const Input = styled('input')({
  display: 'none',
});


export const UploadButton = (props) => {
  return (
    <StyledEngineProvider injectFirst>
      <label htmlFor="contained-button-file">
        <Input accept="image/*" id="contained-button-file" multiple type="file" />
        <Button component='span' className={props.buttonType + ' button-upload'} variant="contained" size='large'>
          {props.buttonText}
        </Button>
      </label>
    </StyledEngineProvider>
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
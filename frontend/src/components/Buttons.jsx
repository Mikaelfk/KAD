import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

const Input = styled('input')({
  display: 'none',
});

export const UploadButton = (props) => {
  return (
      <label htmlFor="contained-button-file">
        <Input accept="image/*" id="contained-button-file" multiple type="file" />
        <Button variant="contained" component="span" className='button-upload'>
          {props.buttonText}
        </Button>
      </label>
  );
}

export const SubmitButton = () => {
  return (<Button size="medium" variant="contained">Submit</Button>);
}

export const CancelButton = (props) => {
  return (<Button size="medium" component={props.component} to={props.to}>Cancel</Button>);
}
import React from 'react';
import { styled, StyledEngineProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import './Buttons.css';

const Input = styled('input')({
    display: 'none',
});


export const UploadButton = (props) => {
    return (
        <StyledEngineProvider injectFirst>
            <form>
                <label htmlFor={"contained-button-file" + props.buttonId}>
                    <Input accept="image/*" id={"contained-button-file" + props.buttonId} multiple type="file" onChange={props.onUpload} />
                    <Button component='span' className={props.buttonType + ' button-upload'} variant="contained" size='large'>
                        {props.buttonText}
                    </Button>
                </label>
            </form>
        </StyledEngineProvider >
    );
}


UploadButton.defaultProps = {
    buttonType: "button"
}

export const SubmitButton = (props) => {
    return (
        <div>
            <Button className='button' size="medium" variant="contained" onClick={props.onSubmit()}>Submit</Button>
        </div>
    );
}

export const CancelButton = (props) => {
    return (<Button size="medium" component={props.component} to={props.to}>Cancel</Button>);
}
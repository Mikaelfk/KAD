import Button from '@mui/material/Button';
import { styled, StyledEngineProvider } from '@mui/material/styles';
import PropTypes from 'prop-types';
import React from 'react';
import './Buttons.css';

const Input = styled('input')({
    display: 'none',
});


export const UploadButton = (props) => {
    let input;
    if (props.uploadTypeSingle === true) {
        input = <Input accept="image/*" id={"contained-button-file" + props.buttonId} type="file" onChange={props.onUpload} />
    } else {
        input = <Input accept="image/*" id={"contained-button-file" + props.buttonId} multiple type="file" onChange={props.onUpload} />
    }
    return (
        <StyledEngineProvider injectFirst>
            <form>
                <label htmlFor={"contained-button-file" + props.buttonId}>
                    {input}
                    <Button component='span' className={props.buttonType + ' button-upload'} variant="contained" size='large'>
                        {props.buttonText}
                    </Button>
                </label>
            </form>
        </StyledEngineProvider >
    );
}

UploadButton.propTypes = {
    uploadTypeSingle: PropTypes.bool,
    onUpload: PropTypes.func.isRequired,
    buttonId: PropTypes.number,
    buttonType: PropTypes.string.isRequired,
    buttonText: PropTypes.string.isRequired
}


UploadButton.defaultProps = {
    buttonType: "button"
}

export const SubmitButton = (props) => {
    return (
        <div>
            <Button
                className='button'
                size="medium"
                variant="contained"
                onClick={props.onSubmit}>
                Submit
            </Button>
        </div>
    );
}

SubmitButton.propTypes = {
    onSubmit: PropTypes.func.isRequired
}

export const CancelButton = (props) => {
    return (
        <Button
            size="medium"
            component={props.component}
            to={props.to}>
            Cancel
        </Button>);
}

CancelButton.propTypes = {
    component: PropTypes.object.isRequired,
    to: PropTypes.string.isRequired
}
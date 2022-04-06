import { FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadObject = (props) => {
    const onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])


    // MenuItems for targets
    const targets = ["TE263", "GTObject"].map((target) => (
        <MenuItem key={target} value={target}>
            {target}
        </MenuItem>
    ));

    // handles target change event
    const handleTargetChange = (event) => {
        props.setTarget(event.target.value)
    }

    return (
        <div className='container'>
            <Typography variant='h2'>Object Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Select images" onUpload={props.onUpload} />
                <Typography sx={{ visibility: "hidden" }} id="images-text">Selected images count: {props.files.length}</Typography>
            </div>
            <div className='target-options'>
                <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose target to perform analysis with">
                    <InputLabel id="target-label">Choose target</InputLabel>
                    <Select value={props.target} onChange={handleTargetChange} labelId="target-label" label="Choose target">
                        {targets}
                    </Select>
                </FormControl>
            </div>
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={props.onSubmit} />
            </div>
            <div className="loader-container" id="loader-container">
                <div className="loader"></div>
            </div>
        </div>
    );
}

UploadObject.propTypes = {
    onRender: PropTypes.func.isRequired,
    onUpload: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired,
    onSubmit: PropTypes.func.isRequired,
    setTarget: PropTypes.func.isRequired,
    target: PropTypes.string.isRequired
}

export default UploadObject;
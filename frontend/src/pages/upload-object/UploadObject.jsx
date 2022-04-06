import { FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadObject = (props) => {
    // resets state variables on render
    useEffect(() => {
        props.setFiles([]);
    }, [])

    const [objectTarget, setObjectTarget] = useState("TE263");

    // MenuItems for targets
    const targets = ["TE263", "GTObject"].map((target) => (
        <MenuItem key={target} value={target}>
            {target}
        </MenuItem>
    ));

    // handles target change event
    const handleTargetChange = (event) => {
        setObjectTarget(event.target.value)
    }

    // handles submit for object level analysis
    const handleObjectSubmit = () => {
        const formData = new FormData();

        // checks if the user has uploaded any files
        if (props.files.length === 0) {
            alert("No files have been selected")
            return
        }

        for (const file of props.files) {
            formData.append('files', file)
        }
        // shows a loading circle
        document.getElementById('loader-container').style.visibility = "visible";
        // Makes a POST request to the endpoint
        props.fetchAnalyzePostWrapper(formData, `/api/analyze/object?iqes=OQT&target=${objectTarget}`)
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
                    <Select value={objectTarget} onChange={handleTargetChange} labelId="target-label" label="Choose target">
                        {targets}
                    </Select>
                </FormControl>
            </div>
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={handleObjectSubmit} />
            </div>
            <div className="loader-container" id="loader-container">
                <div className="loader"></div>
            </div>
        </div>
    );
}

UploadObject.propTypes = {
    onUpload: PropTypes.func.isRequired,
    fetchAnalyzePostWrapper: PropTypes.func.isRequired,
    setFiles: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired
}

export default UploadObject;
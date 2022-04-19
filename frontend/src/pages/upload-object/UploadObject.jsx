import { FormGroup, FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';
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

    const targetData = [
        {
            target: "GTObject",
            software: ["OS QM-Tool"]
        },
        {
            target: "TE263",
            software: ["OS QM-Tool"]
        }
    ]
    // stores acronyms for each software
    const softwareAcronyms = [
        {
            software: "OS QM-Tool",
            acronym: "OQT"
        }
    ]
    // state variable for the software and target chosen
    const [{ software, target: objectTarget }, setData] = useState({
        software: "OS QM-Tool",
        target: "TE263"
    });

    // MenuItems for targets
    const targets = targetData.map((data) => (
        <MenuItem key={data.target} value={data.target}>
            {data.target}
        </MenuItem>
    ));

    // defines what softwares are available for each target
    const softwares = targetData.find(item => item.target === objectTarget)?.software.map((softwareTemp) => (
        <MenuItem key={softwareTemp} value={softwareTemp}>
            {softwareTemp}
        </MenuItem>
    ));
    // handles target change event
    const handleTargetChange = (event) => {
        setData({
            software: "OS QM-Tool",
            target: event.target.value
        })
    }

    const handleSoftwareChange = (event) => {
        setData(data => ({
            ...data,
            software: event.target.value
        }))
    }

    // handles submit for object level analysis
    const handleObjectSubmit = () => {
        const formData = new FormData();

        // checks if the user has uploaded any files
        if (props.files.length === 0) {
            alert("No files have been selected");
            return;
        }

        for (const file of props.files) {
            formData.append('files', file);
        }
        // shows a loading circle
        document.getElementById('loader-container').style.visibility = "visible";


        // finds software acronym based on the software name
        // the acronym is used in the api call
        const softwareAcronym = softwareAcronyms.find(item => item.software === software).acronym;

        // Makes a POST request to the endpoint
        props.fetchAnalyzePostWrapper(formData, `/api/analyze/object?iqes=${softwareAcronym}&target=${objectTarget}`);
    }

    return (
        <div className='container'>
            <Typography variant='h2'>Object Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Select images" onUpload={props.onUpload} />
                <Typography sx={{ visibility: "hidden" }} id="images-text">Selected images count: {props.files.length}</Typography>
            </div>
            <div className='target-options'>
                <FormGroup>
                    <div>
                        <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose target to perform analysis with">
                            <InputLabel id="target-label">Choose target</InputLabel>
                            <Select value={objectTarget} onChange={handleTargetChange} labelId="target-label" label="Choose target">
                                {targets}
                            </Select>
                        </FormControl>
                    </div>
                    <div>
                        <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose analysis software to perform analysis with">
                            <InputLabel id="software-label">Choose analysis software</InputLabel>
                            <Select value={software} onChange={handleSoftwareChange} labelId="software-label" label="Choose analysis software">
                                {softwares}
                            </Select>
                        </FormControl>
                    </div>
                </FormGroup>
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
import { FormGroup, IconButton, FormControl, Select, InputLabel, MenuItem, Typography } from '@mui/material';
import HelpIcon from '@mui/icons-material/Help';
import PropTypes from 'prop-types';
import { React, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadDevice = (props) => {

    // Resets state variables on render
    useEffect(() => {
        props.setFiles([]);
        setStartTarget({})
        setEndTarget({})
    }, [])

    // variable for what softwares support what targets
    const softwareData = [
        {
            name: "IQ-Analyzer-X",
            value: "IQX",
            targets: ["UTT"]
        },
        {
            name: "OS QM-Tool",
            value: "OQT",
            targets: ["UTT", "GTDevice"]
        }
    ];

    const [{ software, target: deviceTarget }, setData] = useState({
        software: "IQX",
        target: "UTT"
    })
    const [startTarget, setStartTarget] = useState({});
    const [endTarget, setEndTarget] = useState({});

    // MenuItems for software select
    const softwares = softwareData.map((data) => (
        <MenuItem key={data.name} value={data.value}>
            {data.name}
        </MenuItem>
    ));

    // MenuItems for target select
    const targets = softwareData.find(item => item.value === software)?.targets.map((target) => (
        <MenuItem key={target} value={target}>
            {target}
        </MenuItem>
    ));

    // handles software change event
    const handleSoftwareChange = (event) => {
        setData({
            software: event.target.value,
            target: "UTT"
        })
    }

    // handles target change event
    const handleTargetChange = (event) => {
        setData(data => ({
            ...data,
            target: event.target.value
        }))
    }

    const handleStartTargetUpload = (event) => {
        document.getElementById("start-target-text").style.visibility = "visible"
        setStartTarget(event.target.files[0])
    }

    const handleEndTargetUpload = (event) => {
        document.getElementById("end-target-text").style.visibility = "visible"
        setEndTarget(event.target.files[0])
    }

    const handleDeviceSubmit = () => {
        // Checks if both targets have been uploaded
        if (startTarget && Object.keys(startTarget).length === 0 && Object.getPrototypeOf(startTarget) === Object.prototype) {
            alert("Start target has not been selected");
            return;
        }
        if (endTarget && Object.keys(endTarget).length === 0 && Object.getPrototypeOf(endTarget) === Object.prototype) {
            alert("End target has not been selected");
            return;
        }

        // Adds the targets as files in a form
        const formData = new FormData();
        formData.append('before_target', startTarget);
        formData.append('after_target', endTarget);

        for (const file of props.files) {
            formData.append('files', file);
        }

        document.getElementById('loader-container').style.visibility = "visible";

        // Makes the request to the api
        props.fetchAnalyzePostWrapper(formData, `/api/analyze/device?iqes=${software}&target=${deviceTarget}`)
    }

    return (
        <div className='container'>
            <Typography variant='h2'>Device Level Target</Typography>
            <div className='upload-options'>
                <div>
                    <UploadButton
                        buttonText="Select start target"
                        buttonType='button-orange'
                        onUpload={handleStartTargetUpload}
                        uploadTypeSingle={true}
                        buttonId={1}
                        title="Upload target scanned before the scanned images" />
                    <Typography sx={{ visibility: "hidden" }} id="start-target-text">Selected start target: {startTarget.name}</Typography>
                </div>
                <div>
                    <UploadButton
                        buttonText="Select end target"
                        buttonType='button-orange'
                        onUpload={handleEndTargetUpload}
                        uploadTypeSingle={true}
                        buttonId={2}
                        title="Upload target scanned after the scanned images" />
                    <Typography sx={{ visibility: "hidden" }} id="end-target-text">Selected end target: {endTarget.name}</Typography>
                </div>
                <div>
                    <div className="upload-images-button-menu">
                        <div className="upload-images-button">
                            <UploadButton className="upload-images-button"
                                buttonText="Select images"
                                onUpload={props.onUpload}
                                buttonId={3}
                                title="Upload the scanned images" />
                        </div>
                        <div className="help-icon">
                            <IconButton sx={{ color: "#1976d2" }}>
                                <HelpIcon />
                            </IconButton>
                            <Typography className="tooltiptext">
                                This is where you upload all images scanned between the two targets uploaded.
                                This upload is optional and is not needed
                            </Typography>
                        </div>
                    </div>
                    <Typography sx={{ visibility: "hidden" }} id="images-text">Selected images count: {props.files.length}</Typography>
                </div>
                <div className='target-options'>
                    <FormGroup>
                        <div>
                            <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose analysis software to perform analysis with">
                                <InputLabel id="software-label">Choose analysis software</InputLabel>
                                <Select value={software} onChange={handleSoftwareChange} labelId="software-label" label="Choose analysis software">
                                    {softwares}
                                </Select>
                            </FormControl>
                        </div>
                        <div>
                            <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose target to perform analysis with">
                                <InputLabel id="target-label">Choose target</InputLabel>
                                <Select value={deviceTarget} onChange={handleTargetChange} labelId="target-label" label="Choose target">
                                    {targets}
                                </Select>
                            </FormControl>
                        </div>
                    </FormGroup>
                </div>
            </div >
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={handleDeviceSubmit} />
            </div>
            <div className="loader-container" id="loader-container">
                <div className="loader"></div>
            </div>
        </div >
    );
}

UploadDevice.propTypes = {
    onUpload: PropTypes.func.isRequired,
    fetchAnalyzePostWrapper: PropTypes.func.isRequired,
    setFiles: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired
}

export default UploadDevice;
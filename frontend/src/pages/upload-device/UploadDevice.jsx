import { FormGroup, IconButton, FormControl, Select, InputLabel, MenuItem, Typography } from '@mui/material';
import HelpIcon from '@mui/icons-material/Help';
import PropTypes from 'prop-types';
import { React, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadDevice = (props) => {

    // resets state variables on render
    useEffect(() => {
        props.setFiles([]);
        setStartTarget({})
        setEndTarget({})
    }, [])

    // variable for what software support what targets
    const targetData = [
        {
            target: "UTT",
            software: ["OS QM-Tool", "IQ-Analyzer-X"]
        },
        {
            target: "GTDevice",
            software: ["OS QM-Tool"]
        }
    ];

    // stores acronyms for each software
    const softwareAcronyms = [
        {
            software: "OS QM-Tool",
            acronym: "OQT"
        },
        {
            software: "IQ-Analyzer-X",
            acronym: "IQX"
        }

    ]

    // state variable for the software and target chosen
    const [{ software, target: deviceTarget }, setData] = useState({
        software: "OS QM-Tool",
        target: "UTT"
    })
    const [startTarget, setStartTarget] = useState({});
    const [endTarget, setEndTarget] = useState({});


    // defines what targets are available for use
    const targets = targetData.map((data) => (
        <MenuItem key={data.target} value={data.target}>
            {data.target}
        </MenuItem>
    ));

    // defines what softwares are available for each target
    const softwares = targetData.find(item => item.target === deviceTarget)?.software.map((softwareTemp) => (
        <MenuItem key={softwareTemp} value={softwareTemp}>
            {softwareTemp}
        </MenuItem>
    ));

    // handles software change event
    const handleSoftwareChange = (event) => {
        setData(data => ({
            ...data,
            software: event.target.value
        }))
    }

    // handles target change event
    const handleTargetChange = (event) => {
        setData({
            software: "OS QM-Tool",
            target: event.target.value
        })
    }

    // handles start target upload and saves it to state variable
    const handleStartTargetUpload = (event) => {
        document.getElementById("start-target-text").style.visibility = "visible"
        setStartTarget(event.target.files[0])
    }

    // handles end target upload and saves it to state variable
    const handleEndTargetUpload = (event) => {
        document.getElementById("end-target-text").style.visibility = "visible"
        setEndTarget(event.target.files[0])
    }

    // handles submit for device level analysis
    const handleDeviceSubmit = () => {
        // checks if both targets have been uploaded
        if (startTarget && Object.keys(startTarget).length === 0 && Object.getPrototypeOf(startTarget) === Object.prototype) {
            alert("Start target has not been selected");
            return;
        }
        if (endTarget && Object.keys(endTarget).length === 0 && Object.getPrototypeOf(endTarget) === Object.prototype) {
            alert("End target has not been selected");
            return;
        }

        // adds the targets as files in a form
        const formData = new FormData();
        formData.append('before_target', startTarget);
        formData.append('after_target', endTarget);
        for (const file of props.files) {
            formData.append('files', file);
        }
        // shows a loading circle
        document.getElementById('loader-container').style.visibility = "visible";

        // finds software acronym based on the software name
        // the acronym is used in the api call
        const softwareAcronym = softwareAcronyms.find(item => item.software === software).acronym;
        console.log(softwareAcronym)

        // makes the request to the api
        props.fetchAnalyzePostWrapper(formData, `/api/analyze/device?iqes=${softwareAcronym}&target=${deviceTarget}`)
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
                            <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose target to perform analysis with">
                                <InputLabel id="target-label">Choose target</InputLabel>
                                <Select value={deviceTarget} onChange={handleTargetChange} labelId="target-label" label="Choose target">
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
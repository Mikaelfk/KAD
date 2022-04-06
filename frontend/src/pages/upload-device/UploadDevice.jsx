import { FormGroup, IconButton, FormControl, Select, InputLabel, MenuItem, Typography } from '@mui/material';
import HelpIcon from '@mui/icons-material/Help';
import PropTypes from 'prop-types';
import { React, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadDevice = (props) => {

    const onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])

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

    // MenuItems for software select
    const softwares = softwareData.map((software) => (
        <MenuItem key={software.name} value={software.value}>
            {software.name}
        </MenuItem>
    ));

    // MenuItems for target select
    const targets = softwareData.find(item => item.value === props.software)?.targets.map((target) => (
        <MenuItem key={target} value={target}>
            {target}
        </MenuItem>
    ));

    // handles software change event
    const handleSoftwareChange = (event) => {
        props.setData({
            software: event.target.value,
            target: "UTT"
        })
    }

    // handles target change event
    const handleTargetChange = (event) => {
        props.setData(data => ({
            ...data,
            target: event.target.value
        }))
    }

    return (
        <div className='container'>
            <Typography variant='h2'>Device Level Target</Typography>
            <div className='upload-options'>
                <div>
                    <UploadButton
                        buttonText="Select start target"
                        buttonType='button-orange'
                        onUpload={props.onStartTargetUpload}
                        uploadTypeSingle={true}
                        buttonId={1}
                        title="Upload target scanned before the scanned images" />
                    <Typography sx={{ visibility: "hidden" }} id="start-target-text">Selected start target: {props.startTarget.name}</Typography>
                </div>
                <div>
                    <UploadButton
                        buttonText="Select end target"
                        buttonType='button-orange'
                        onUpload={props.onEndTargetUpload}
                        uploadTypeSingle={true}
                        buttonId={2}
                        title="Upload target scanned after the scanned images" />
                    <Typography sx={{ visibility: "hidden" }} id="end-target-text">Selected end target: {props.endTarget.name}</Typography>
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
                                <Select value={props.software} onChange={handleSoftwareChange} labelId="software-label" label="Choose analysis software">
                                    {softwares}
                                </Select>
                            </FormControl>
                        </div>
                        <div>
                            <FormControl sx={{ m: 1, minWidth: 170 }} aria-label="Choose target to perform analysis with">
                                <InputLabel id="target-label">Choose target</InputLabel>
                                <Select value={props.target} onChange={handleTargetChange} labelId="target-label" label="Choose target">
                                    {targets}
                                </Select>
                            </FormControl>
                        </div>
                    </FormGroup>
                </div>
            </div >
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={props.onSubmit} />
            </div>
            <div className="loader-container" id="loader-container">
                <div className="loader"></div>
            </div>
        </div >
    );
}

UploadDevice.propTypes = {
    onRender: PropTypes.func.isRequired,
    onStartTargetUpload: PropTypes.func.isRequired,
    startTarget: PropTypes.object.isRequired,
    onEndTargetUpload: PropTypes.func.isRequired,
    endTarget: PropTypes.object.isRequired,
    onUpload: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired,
    onSubmit: PropTypes.func.isRequired,
    software: PropTypes.string.isRequired,
    target: PropTypes.string.isRequired,
    setData: PropTypes.func.isRequired
}

export default UploadDevice;
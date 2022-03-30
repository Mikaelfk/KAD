import { Typography } from '@mui/material';
import PropTypes from 'prop-types';
import { React, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadDevice = (props) => {
    let onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])

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
                    <Typography>Selected start target: {props.startTarget.name}</Typography>
                </div>
                <div>
                    <UploadButton
                        buttonText="Select end target"
                        buttonType='button-orange'
                        onUpload={props.onEndTargetUpload}
                        uploadTypeSingle={true}
                        buttonId={2}
                        title="Upload target scanned after the scanned images" />
                    <Typography>Selected end target: {props.endTarget.name}</Typography>
                </div>
                <div>
                    <UploadButton
                        buttonText="Select images"
                        onUpload={props.onUpload}
                        buttonId={3}
                        title="Upload the scanned images" />
                    <Typography>Selected images count: {props.files.length}</Typography>
                </div>
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

UploadDevice.propTypes = {
    onRender: PropTypes.func.isRequired,
    onStartTargetUpload: PropTypes.func.isRequired,
    startTarget: PropTypes.object.isRequired,
    onEndTargetUpload: PropTypes.func.isRequired,
    endTarget: PropTypes.object.isRequired,
    onUpload: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired,
    onSubmit: PropTypes.func.isRequired
}

export default UploadDevice;
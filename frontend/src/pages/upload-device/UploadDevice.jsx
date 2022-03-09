import React, { useEffect } from 'react';
import { Typography } from '@mui/material';
import { UploadButton, SubmitButton, CancelButton } from '../../components/Buttons';
import { Link } from 'react-router-dom';
import '../Upload.css'

const UploadDevice = (props) => {
    let onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])

    return (
        <div className='container'>
            <Typography variant='h2'>Device Level Target</Typography>
            <div className='upload-options'>
                <UploadButton
                    buttonText="Velg start target"
                    buttonType='button-orange'
                    onUpload={props.onStartTargetUpload}
                    uploadTypeSingle={true}
                    buttonId={1} />
                    <Typography>Start target valgt: {props.startTarget.name}</Typography>
                <UploadButton
                    buttonText="Velg slutt target"
                    buttonType='button-orange'
                    onUpload={props.onEndTargetUpload}
                    uploadTypeSingle={true}
                    buttonId={2} />
                    <Typography>End target valgt: {props.endTarget.name}</Typography>
                <UploadButton
                    buttonText="Velg bilder"
                    onUpload={props.onUpload}
                    buttonId={3} />
                    <Typography>Antall bilder valgt: {props.files.length}</Typography>
            </div>
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={props.onSubmit} />
            </div>
        </div>
    );
}

export default UploadDevice;
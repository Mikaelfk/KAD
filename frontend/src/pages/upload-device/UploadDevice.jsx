import React from 'react';
import { Typography } from '@mui/material';
import { UploadButton, SubmitButton, CancelButton } from '../../components/Buttons';
import { Link } from 'react-router-dom';
import '../Upload.css'

const UploadDevice = (props) => {
    return (
        <div className='container'>
            <Typography variant='h2'>Device Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Velg start target" buttonType='button-orange' onUpload={props.onStartTargetUpload} buttonId={1}/>
                <UploadButton buttonText="Velg slutt target" buttonType='button-orange' onUpload={props.onEndTargetUpload} buttonId={2} />
                <UploadButton buttonText="Velg bilder" onUpload={props.onUpload} buttonId={3} />
            </div>
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={props.onSubmit} />
            </div>
        </div>
    );
}

export default UploadDevice;
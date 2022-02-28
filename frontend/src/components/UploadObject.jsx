import React from 'react';
import { Typography } from '@mui/material';
import { UploadButton, SubmitButton, CancelButton } from './Buttons';
import './UploadObject.css';

const UploadObject = () => {
    return (
        <div className='container'>
            <Typography variant='h2'>Object Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Velg bilder" />
            </div>
            <div className='action-menu'>
                <CancelButton />
                <SubmitButton />
            </div>
        </div>
    );
}

export default UploadObject;
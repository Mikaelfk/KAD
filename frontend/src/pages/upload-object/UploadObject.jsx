import React, { useEffect } from 'react';
import { Typography } from '@mui/material';
import { UploadButton, SubmitButton, CancelButton } from '../../components/Buttons';
import { Link } from 'react-router-dom';
import '../Upload.css'

const UploadObject = (props) => {
    let onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])

    return (
        <div className='container'>
            <Typography variant='h2'>Object Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Velg bilder" onUpload={props.onUpload} />
                <Typography>Antall bilder valgt: {props.files.length}</Typography>
            </div>
            <div className='action-menu'>
                <CancelButton component={Link} to='/' />
                <SubmitButton onSubmit={props.onSubmit} />
            </div>
        </div>
    );
}

export default UploadObject;
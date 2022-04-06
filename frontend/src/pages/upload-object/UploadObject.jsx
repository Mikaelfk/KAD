import { Typography } from '@mui/material';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { CancelButton, SubmitButton, UploadButton } from '../../components/Buttons';
import '../Upload.css';

const UploadObject = (props) => {
    const onRender = props.onRender;
    useEffect(() => {
        onRender()
    }, [onRender])


    const targets = ["TE263", "GTObject"].map((target) => (
    <option key={target} value={target}>
      {target}
    </option>
  ));

    const handleTargetChange = (event) => {
        props.setTarget(event.target.value)
    }

    return (
        <div className='container'>
            <Typography variant='h2'>Object Level Target</Typography>
            <div className='upload-options'>
                <UploadButton buttonText="Select images" onUpload={props.onUpload} />
                <Typography sx={{ visibility: "hidden" }} id="images-text">Selected images count: {props.files.length}</Typography>
            </div>
            <div className='container'>
                <Typography>Choose target</Typography>
                <form>
                    <div>
                        <select onChange={handleTargetChange}>
                            {targets}
                        </select>
                    </div>
                </form>
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

UploadObject.propTypes = {
    onRender: PropTypes.func.isRequired,
    onUpload: PropTypes.func.isRequired,
    files: PropTypes.array.isRequired,
    onSubmit: PropTypes.func.isRequired,
    setTarget: PropTypes.func.isRequired,
}

export default UploadObject;
import React, { useState } from 'react';
import {
    BrowserRouter, Route, Routes
} from 'react-router-dom';
import MainPage from './pages/main-page/MainPage';
import UploadDevice from './pages/upload-device/UploadDevice';
import UploadObject from './pages/upload-object/UploadObject';
import configData from './config.json'

const App = () => {

    const [files, setFiles] = useState([]);
    const [startTarget, setStartTarget] = useState({});
    const [endTarget, setEndTarget] = useState({});

    const handleUpload = (event) => {
        const inputFiles = event.target.files
        // Empty array before adding files
        setFiles([])
        // Add each file to the array
        for (const inputFile of inputFiles) {
            setFiles(arr => [...arr, inputFile])
        }
    }

    const handleStartTargetUpload = (event) => {
        setStartTarget(event.target.files[0])
    }

    const handleEndTargetUpload = (event) => {
        setEndTarget(event.target.files[0])
    }

    const handleObjectSubmit = () => {
        const formData = new FormData();
        const fileField = document.querySelector('input[type="file"]');

        formData.append('file', fileField.files[0]);
        // Makes a POST request to the endpoint,
        // TODO: Change endpoint to image quality assessment instead of file validation endpoint.
        fetch(configData.API_URL + '/api/validate', {
            method: 'POST',
            body: formData
        })
            .then(result => {
                console.log('Success:', result.text());
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    const handleDeviceSubmit = (event) => {
        console.log(startTarget)
        console.log(endTarget)
        console.log(files)
        // TODO: Make this when we have made the image quality assessment endpoint
    }
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<MainPage />} />
                <Route path="/upload/device" element=
                    {<UploadDevice
                        onUpload={handleUpload}
                        onStartTargetUpload={handleStartTargetUpload}
                        onEndTargetUpload={handleEndTargetUpload}
                        onSubmit={handleDeviceSubmit} />} />
                <Route path="/upload/object" element=
                    {<UploadObject
                        onUpload={handleUpload}
                        onSubmit={handleObjectSubmit} />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

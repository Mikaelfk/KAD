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
    const handleUpload = (event) => {
        const inputFiles = event.target.files
        // Empty array before adding files
        setFiles([])
        // Add each file to the array
        for (const inputFile of inputFiles) {
            setFiles(arr => [...arr, inputFile])
        }
    }

    const handleSubmit = (event) => {
        const formData = new FormData();
        const fileField = document.querySelector('input[type="file"]');

        console.log(fileField.files[0])
        formData.append('file', fileField.files[0]);
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
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<MainPage />} />
                <Route path="/upload/device" element={<UploadDevice onClick={handleUpload} onSubmit={handleSubmit} files={files}/>} />
                <Route path="/upload/object" element={<UploadObject onClick={handleUpload} onSubmit={handleSubmit} files={files}/>} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

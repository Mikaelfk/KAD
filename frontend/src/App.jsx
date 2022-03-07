import React, { useState } from 'react';
import {
    Route, Routes, useNavigate
} from 'react-router-dom';
import MainPage from './pages/main-page/MainPage';
import UploadDevice from './pages/upload-device/UploadDevice';
import UploadObject from './pages/upload-object/UploadObject';
import ResultsPage from './pages/results-page/ResultsPage';
import ResultPage from './pages/result-page/ResultPage'

const App = () => {

    const [files, setFiles] = useState([]);
    const [startTarget, setStartTarget] = useState({});
    const [endTarget, setEndTarget] = useState({});

    let navigate = useNavigate()

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
        let resultId = 100
        // Makes a POST request to the endpoint,
        // TODO: Change endpoint to image quality assessment
        fetch('/endpoint/path', {
            method: 'POST',
            body: formData
        })
            .then(result => {
                console.log('Success:', result.text());
                let path = `/results/${resultId}`
                navigate(path)
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    const handleDeviceSubmit = () => {
        console.log(startTarget)
        console.log(endTarget)
        console.log(files)
        let resultId = 100
        // TODO: Set correct path here
        fetch('/endpoint/path')
            .then(data => {
                console.log(data)
                // TODO: set resultId to what the request response gives.
                let path = `/results/${resultId}`
                navigate(path)
            })
            .catch(err => console.log(err))
    }

    return (
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
            <Route path="/results/:resultId" element={<ResultsPage />} />
            <Route path="/result/:imageId" element={<ResultPage />} />
        </Routes>
    );
}

export default App;

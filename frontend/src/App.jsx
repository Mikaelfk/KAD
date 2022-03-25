import React, { useCallback, useState } from 'react';
import {
    Route, Routes, useNavigate
} from 'react-router-dom';
import MainPage from './pages/main-page/MainPage';
import UploadDevice from './pages/upload-device/UploadDevice';
import UploadObject from './pages/upload-object/UploadObject';
import ResultsPage from './pages/results-page/ResultsPage';
import ResultPage from './pages/result-page/ResultPage'
import Config from "./config.json"

const App = () => {

    const [files, setFiles] = useState([]);
    const [startTarget, setStartTarget] = useState({});
    const [endTarget, setEndTarget] = useState({});

    let navigate = useNavigate()

    const handleRender = useCallback(() => {
        setFiles([])
        setStartTarget({})
        setEndTarget({})
    }, []);

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
        let sessionId = 100
        // Makes a POST request to the endpoint,
        // TODO: Change endpoint to image quality assessment

        fetch(Config.API_URL + '', {
            method: 'POST',
            body: formData
        })
            .then(result => {
                console.log('Success:', result.text());
                let path = `/results/${sessionId}`
                navigate(path)
            })
            .catch(error => {
                console.error('Error:', error);
            });

    }

    const handleDeviceSubmit = () => {
        const formData = new FormData();

        // Adds the targets as files in a form
        formData.append('before_target', startTarget);
        formData.append('after_target', endTarget);
        for (const file of files) {
            formData.append('files', file)
        }

        document.getElementById('loader-container').style.visibility = "visible";

        // Makes the request to the api
        fetch(Config.API_URL + '/api/analyze/device/iqx?target=UTT', {
            method: 'POST',
            body: formData
        })
            .then(resp => resp.json())
            .then(data => {
                document.getElementById('loader-container').style.visibility = "hidden";

                let path = `/results/${data.session_id}`;
                navigate(path);
            })
            .catch(err => console.log(err))
    }

    return (
        <Routes>
            <Route exact path="/" element={<MainPage />} />
            <Route path="/upload/device" element=
                {<UploadDevice
                    onRender={handleRender}
                    onUpload={handleUpload}
                    onStartTargetUpload={handleStartTargetUpload}
                    onEndTargetUpload={handleEndTargetUpload}
                    onSubmit={handleDeviceSubmit}
                    startTarget={startTarget}
                    endTarget={endTarget}
                    files={files} />} />
            <Route path="/upload/object" element=
                {<UploadObject
                    onRender={handleRender}
                    onUpload={handleUpload}
                    onSubmit={handleObjectSubmit}
                    files={files} />} />
            <Route path="/results/:session_id" element={<ResultsPage />} />
            <Route path="/results/:session_id/:imageId" element={<ResultPage />} />
        </Routes>
    );
}

export default App;

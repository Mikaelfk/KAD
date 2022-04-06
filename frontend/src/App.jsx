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
    const [target, setTarget] = useState("TE263");

    let navigate = useNavigate()

    const handleRender = useCallback(() => {
        setFiles([])
        setStartTarget({})
        setEndTarget({})
    }, []);

    const fetchAnalyzePostWrapper = (formData, uri) => {
        fetch(Config.API_URL + uri, {
            method: 'POST',
            body: formData
        })
            .then(resp => resp.json())
            .then(data => {
                document.getElementById('loader-container').style.visibility = "hidden";
                let path = `/results/${data.session_id}`;
                navigate(path);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loader-container').style.visibility = "hidden";
            });
    }
    
    const handleUpload = (event) => {
        document.getElementById("images-text").style.visibility = "visible"
        const inputFiles = event.target.files
        // Empty array before adding files
        setFiles([])
        // Add each file to the array
        for (const inputFile of inputFiles) {
            setFiles(arr => [...arr, inputFile])
        }
    }

    const handleStartTargetUpload = (event) => {
        document.getElementById("start-target-text").style.visibility = "visible"
        setStartTarget(event.target.files[0])
    }

    const handleEndTargetUpload = (event) => {
        document.getElementById("end-target-text").style.visibility = "visible"
        setEndTarget(event.target.files[0])
    }

    const handleObjectSubmit = () => {
        const formData = new FormData();

        // Checks if the user has uploaded any files
        if (files.length === 0) {
            alert("No files have been selected")
            return
        }

        for (const file of files) {
            formData.append('files', file)
        }

        document.getElementById('loader-container').style.visibility = "visible";
        // Makes a POST request to the endpoint
        fetchAnalyzePostWrapper(formData, `/api/analyze/oqt?target=${target}`)
    }

    const handleDeviceSubmit = () => {
        // Checks if both targets have been uploaded
        if (startTarget && Object.keys(startTarget).length === 0 && Object.getPrototypeOf(startTarget) === Object.prototype) {
            alert("Start target has not been selected");
            return;
        }
        if (endTarget && Object.keys(endTarget).length === 0 && Object.getPrototypeOf(endTarget) === Object.prototype) {
            alert("End target has not been selected");
            return;
        }

        // Adds the targets as files in a form
        const formData = new FormData();
        formData.append('before_target', startTarget);
        formData.append('after_target', endTarget);

        for (const file of files) {
            formData.append('files', file);
        }

        document.getElementById('loader-container').style.visibility = "visible";

        // Makes the request to the api
        fetchAnalyzePostWrapper(formData, '/api/analyze/iqx?target=UTT')
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
                    setTarget={setTarget}
                    files={files} />} />
            <Route path="/results/:session_id" element=
                {<ResultsPage />} />
            <Route path="/results/:session_id/:image_id" element={<ResultPage />} />
        </Routes>
    );
}

export default App;

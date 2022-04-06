import React, { useState } from 'react';
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

    let navigate = useNavigate()

    // performs a POST request to given uri with given form data
    const fetchAnalyzePostWrapper = (formData, uri) => {
        fetch(Config.API_URL + uri, {
            method: 'POST',
            body: formData
        })
            .then(resp => resp.json())
            .then(data => {
                document.getElementById('loader-container').style.visibility = "hidden";
                if (data.error) {
                    alert(data.error)
                    return
                }
                let path = `/results/${data.session_id}`;
                navigate(path);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loader-container').style.visibility = "hidden";
            });
    }

    // handles files upload and saves the files to state variable
    const handleUpload = (event) => {
        document.getElementById("images-text").style.visibility = "visible"
        const inputFiles = event.target.files
        // empty array before adding files
        setFiles([])
        // add each file to the array
        for (const inputFile of inputFiles) {
            setFiles(arr => [...arr, inputFile])
        }
    }

    return (
        <Routes>
            <Route exact path="/" element={<MainPage />} />
            <Route path="/upload/device" element=
                {<UploadDevice
                    onUpload={handleUpload}
                    fetchAnalyzePostWrapper={fetchAnalyzePostWrapper}
                    setFiles={setFiles}
                    files={files} />} />
            <Route path="/upload/object" element=
                {<UploadObject
                    onUpload={handleUpload}
                    fetchAnalyzePostWrapper={fetchAnalyzePostWrapper}
                    setFiles={setFiles}
                    files={files} />} />
            <Route path="/results/:session_id" element=
                {<ResultsPage />} />
            <Route path="/results/:session_id/:image_id" element={<ResultPage />} />
        </Routes>
    );
}

export default App;

import {
    BrowserRouter, Route, Routes
} from 'react-router-dom';
import MainPage from './pages/main-page/MainPage';
import UploadDevice from './pages/upload-device/UploadDevice';
import UploadObject from './pages/upload-object/UploadObject';

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<MainPage />} />
                <Route path="/upload/device" element={<UploadDevice />} />
                <Route path="/upload/object" element={<UploadObject />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

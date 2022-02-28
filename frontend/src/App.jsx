import {
    BrowserRouter, Route, Routes
} from 'react-router-dom';
import MainPage from './components/MainPage';
import UploadDevice from './components/UploadDevice';
import UploadObject from './components/UploadObject';

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

import {
    BrowserRouter, Route, Routes
} from 'react-router-dom';
import './App.css';
import MainPage from './components/MainPage';
import UploadDevice from './components/UploadDevice';

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<MainPage />} />
                <Route path="/upload/device" element={<UploadDevice />} />
                <Route path="/upload/object" element={<UploadDevice />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

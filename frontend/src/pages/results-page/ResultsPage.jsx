import DownloadIcon from '@mui/icons-material/Download';
import EmojiPeopleIcon from '@mui/icons-material/EmojiPeople';
import { Card, CardContent, Divider, IconButton, Typography } from "@mui/material";
import { React, useEffect, useState } from "react";
import { Link, useParams } from 'react-router-dom';
import HomeButton from "../../components/HomeButton";
import Config from "../../config.json";
import "./ResultsPage.css";

const ResultsPage = () => {

    const [results, setResults] = useState({});
    const [status, setStatus] = useState("");
    const [downloadReady, setDownloadReady] = useState(false)

    let params = useParams();
    useEffect(() => {
        // Fetches the status of the session
        fetch(Config.API_URL + `/api/session/status/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => {
                setStatus(data.session_status)
                setDownloadReady((data.session_status == "finished"))
            })
            .catch(err => console.log(err));
        // Fetches the results from the api
        fetch(Config.API_URL + `/api/results/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.session_id])


    // Downloads the images.zip file from a session
    const handleDownloadAll = () => {
        fetch(Config.API_URL + `/api/download/${params.session_id}`)
            .then(resp => {
                if (resp.status != 200) {
                    throw "download is not ready"
                }

                return resp.blob()
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                // the filename you want
                a.download = 'images.zip';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(err => console.log(err))
    }

    const generateList = () => {
        if ((Object.keys(results).length == 0) || results["error"]) {
            // return error
            return (
                <div>
                    <Typography variant="h3">
                        No results
                    </Typography>
                </div>
            )
        }

        return Object.keys(results).map((key) =>
            <Card
                className="resultCard"
                component={Link}
                to={`/results/${params.session_id}/${key}`}
                key={key}
                style={{ textDecoration: 'none' }}
                title="View analysis details"
                aria-label="Field which shows image and analysis results, can be clicked on to view analysis details">
                <CardContent className="result">
                    <Typography variant="h5">
                        Name: {key}
                    </Typography>
                    <Divider flexItem />
                    <Typography variant="h5">
                        ISO score: {results[key].overall_score}
                    </Typography>
                </CardContent>
            </Card>
        )
    }

    return (
        <div className="container">
            <div className="top-bar">
                <IconButton className="hidden" aria-label="Invisible button for positioning" size="large">
                    <EmojiPeopleIcon fontSize='large' />
                </IconButton>
                <HomeButton aria-label="Button for going back to the home page" ></HomeButton>
                <IconButton
                    aria-label="button for downloading all analysed files"
                    size="large"
                    sx={{ color: "#1976d2" }}
                    onClick={handleDownloadAll}
                    title="Download all images"
                    disabled={!downloadReady}>
                    <DownloadIcon fontSize='large' />
                </IconButton>
            </div>
            <Typography variant='h2'>Results</Typography>
            <Typography variant="h5">Session ID: {params.session_id}</Typography>
            <Typography variant="h5">Session Status: {status}</Typography>
            {generateList()}
        </div>
    )
}

export default ResultsPage;
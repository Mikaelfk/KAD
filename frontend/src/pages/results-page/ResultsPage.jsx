import { Card, CardContent, Divider, IconButton, Typography } from "@mui/material";
import { React, useEffect, useState } from "react";
import { Link, useParams } from 'react-router-dom';
import EmojiPeopleIcon from '@mui/icons-material/EmojiPeople';
import DownloadIcon from '@mui/icons-material/Download';
import HomeButton from "../../components/HomeButton";
import Config from "../../config.json";
import "./ResultsPage.css";

const ResultsPage = () => {

    const [results, setResults] = useState({})

    let params = useParams();
    useEffect(() => {
        // Fetches the results from the api
        fetch(Config.API_URL + `/api/results/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.session_id])


    // Downloads the images.zip file from a session
    const handleDownloadAll = () => {
        fetch(Config.API_URL + `/api/download/${params.session_id}`)
            .then(resp => resp.blob())
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

    return (
        <div className="container">
            <div className="top-bar">
                <IconButton className="hidden" aria-label="Invisible button for positioning" size="large">
                    <EmojiPeopleIcon fontSize='large' />
                </IconButton>
                <HomeButton></HomeButton>
                <IconButton aria-label="Download button" size="large" sx={{ color: "#1976d2" }} onClick={handleDownloadAll}>
                    <DownloadIcon fontSize='large' />
                </IconButton>
            </div>
            <Typography variant='h2'>Results</Typography>
            {Object.keys(results).map((key) =>
                <Card className="resultCard" component={Link} to={`/results/${params.session_id}/${key}`} key={key} style={{ textDecoration: 'none' }}>
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
            )}
        </div>
    )
}

export default ResultsPage;
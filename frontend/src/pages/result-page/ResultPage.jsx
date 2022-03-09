import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Typography, IconButton } from "@mui/material";
import HomeButton from "../../components/HomeButton";
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import "./ResultPage.css"

const ResultPage = () => {

    const [imageResult, setImageResult] = useState({ name: "image.jpg", session_id: "100" });

    let params = useParams();
    useEffect(() => {
        // Do a request to get information about a single image based on the id.
        console.log(params.imageId)
        // TODO: Set correct endpoint path
        fetch("/path/to/api")
            .then(resp => resp.json())
            .then(data => setImageResult(data))
            .catch(err => console.log(err))
    }, [params.imageId])

    // TODO: make home button on this page
    return (
        <div className="container" >
            <HomeButton></HomeButton>
            <Typography variant="h2">
                Resultat: {imageResult.name}
            </Typography>
            <div>
                <p>Result goes here</p>
            </div>
            <div className="backButtonContainer">
                <IconButton color="primary" aria-label="upload picture" component={Link} to={`/results/${imageResult.session_id}`} size="large">
                    <ArrowBackIosIcon fontSize="large" />
                </IconButton>
            </div>
        </div>
    )
}

export default ResultPage;
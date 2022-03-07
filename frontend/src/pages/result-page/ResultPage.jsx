import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Typography } from "@mui/material";

const ResultPage = () => {

    const [imageResult, setImageResult] = useState({name: "image.jpg"});

    let params = useParams();
    useEffect(() => {
        // Do a request to get information about a single image based on the id.
        console.log(params.imageId)
        fetch("/path/to/api")
            .then(resp => resp.json())
            .then(data => setImageResult(data))
            .catch(err => console.log(err))
    }, [params.imageId])
    return (
        <div className="container" >
            <Typography variant="h2">
                Resultat: {imageResult.name}
            </Typography>
        </div>
    )
}

export default ResultPage;
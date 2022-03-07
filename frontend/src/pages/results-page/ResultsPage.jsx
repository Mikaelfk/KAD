import { useEffect, useState } from "react";
import { Link, useParams } from 'react-router-dom';
import { Typography, Card, CardContent } from "@mui/material";
import "./ResultsPage.css"

const ResultsPage = () => {

    // Makes an example result for testing
    const [results, setResults] = useState([{ id: "1", imageName: "image.jpg", isoScore: "A" }, { id: "2", imageName: "image2.jpg", isoScore: "B" }])

    let params = useParams();
    useEffect(() => {
        // params.resultId will be used to make the request
        console.log(params.resultId)
        // TODO: Set correct path to endpoint 
        fetch("/path/to/api")
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.resultId])

    return (
        <div className="container">
            <Typography variant='h2'>Resultater</Typography>
            {results.map((result) =>
                <Card className="resultCard" component={Link} to={`/result/${result.id}`} key={result.id} style={{ textDecoration: 'none' }}>
                    <CardContent className="result">
                        <Typography variant="h5">
                        Name: {result.imageName}
                        </Typography>
                        <Typography variant="h5">
                        ISO score: {result.isoScore}
                        </Typography>
                    </CardContent>
                </Card>
            )}
        </div>
    )
}



export default ResultsPage;
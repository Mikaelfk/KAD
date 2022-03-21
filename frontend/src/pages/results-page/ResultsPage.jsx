import { React, useEffect, useState } from "react";
import { Link, useParams } from 'react-router-dom';
import { Typography, Card, CardContent } from "@mui/material";
import HomeButton from "../../components/HomeButton";
import "./ResultsPage.css"
import Config from "../../config.json"

const ResultsPage = () => {

    // Makes an example result for testing
    const [results, setResults] = useState({})


    let params = useParams();
    useEffect(() => {
        // params.resultId will be used to make the request
        fetch(Config.API_URL + `/api/results/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.session_id])


    // TODO: make home button on this page
    return (
        <div className="container">
            <HomeButton></HomeButton>
            <Typography variant='h2'>Resultater</Typography>
            {console.log(results)}
            {Object.keys(results).map((key) =>
                <Card className="resultCard" component={Link} to={`/results/${params.session_id}/${key}`} key={key} style={{ textDecoration: 'none' }}>
                    <CardContent className="result">
                        <Typography variant="h5">
                            Name: {key}
                        </Typography>
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
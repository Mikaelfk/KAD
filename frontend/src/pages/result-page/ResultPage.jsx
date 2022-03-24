import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import EmojiPeopleIcon from '@mui/icons-material/EmojiPeople';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, IconButton, Typography } from "@mui/material";
import React, { useEffect, useState } from 'react';
import { Link, useParams } from "react-router-dom";
import HomeButton from "../../components/HomeButton";
import Config from "../../config.json";
import "./ResultPage.css";

const ResultPage = () => {

    const [results, setResults] = useState({})

    let params = useParams();
    useEffect(() => {
        // params.session_id will be used to make the request
        fetch(Config.API_URL + `/api/results/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.session_id, params.imageId])

    let generateResults = () => {
        // first do checks for smthn wrong and if wrong return no results
        if ((Object.keys(results).length == 0) || results["error"] || !results[params.imageId]) {
            // return error :O
            return (
                <div>
                    <Typography variant="h3">
                        No results :(
                    </Typography>
                </div>
            )
        }

        // results teim :)

        return <div className="results">
            {
                // loop over specification levels
                Object.keys(results[params.imageId])
                    // only get A B C sections
                    .filter(specification_level => (
                        (specification_level != "image_tag") && (specification_level != "overall_score"))
                    )
                    // A, B C instead of C, B, A
                    .reverse()
                    .map((specification_level) =>
                        <Accordion className='category-accordion' key={specification_level}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <div style={{ width: "100%", display: "flex", justifyContent: "space-between" }}>
                                    <Typography variant="h5" display="inline">
                                        {specification_level}
                                    </Typography>
                                    <Typography variant="h5" display="inline">
                                        {
                                            "Passed: " +
                                            (results[params.imageId][specification_level]["results"]["passed"] ? "Yes" : "No")
                                        }
                                    </Typography>
                                </div>
                            </AccordionSummary>
                            <AccordionDetails>
                                {
                                    generateResultsAccordion(results[params.imageId][specification_level]["results"])
                                }
                            </AccordionDetails>
                        </Accordion >
                    )
            }
        </div >
    }

    let generateResultsAccordion = (resultData) => {
        // loop over result categories
        return Object.keys(resultData)
            // not care about passed/not passed here
            .filter((result_category) => result_category != "passed")
            .map((result_category) =>
                <Accordion className="result-accordion" key={result_category}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="h6">
                            {result_category}
                        </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        {
                            // loop over category specific results
                            Object.keys(resultData[result_category])
                                .map((detailed_result) =>
                                    <Typography variant="h6" key={detailed_result}>
                                        {
                                            detailed_result +
                                            ": " +
                                            resultData[result_category][detailed_result]
                                        }
                                    </Typography>
                                )
                        }
                    </AccordionDetails>
                </Accordion>
            )
    }

    return (
        <div className="container" >
            <div className="top-bar">
                <IconButton color="primary" aria-label="Return to result page" component={Link} to={`/results/${params.session_id}`} size="large">
                    <ArrowBackIosIcon fontSize="large" />
                </IconButton>
                <HomeButton></HomeButton>
                <IconButton className="hidden" aria-label="Invisible button for positioning" size="large">
                    <EmojiPeopleIcon fontSize='large' />
                </IconButton>
            </div>

            <Typography variant="h2">
                Resultat: {params.imageId}
            </Typography>

            {
                generateResults()
            }

            <div className="backButtonContainer">

            </div>
        </div>
    )
}

export default ResultPage;
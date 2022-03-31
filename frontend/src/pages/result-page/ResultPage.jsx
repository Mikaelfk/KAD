import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import DownloadIcon from '@mui/icons-material/Download';
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
        // Fetches the results from the api
        fetch(Config.API_URL + `/api/results/${params.session_id}`)
            .then(resp => resp.json())
            .then(data => setResults(data))
            .catch(err => console.log(err))
    }, [params.session_id, params.image_id])

    // Downloads the images.zip file from a session
    const handleDownload = () => {
        fetch(Config.API_URL + `/api/download/${params.session_id}?file_name=${params.image_id}`)
            .then(resp => resp.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                // the filename you want
                a.download = params.image_id;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(err => console.log(err))
    }

    const generateResults = () => {
        // first do checks for smthn wrong and if wrong return no results
        if ((Object.keys(results).length == 0) || results["error"] || !results[params.image_id]) {
            // return error
            return (
                <div>
                    <Typography variant="h3">
                        No results :(
                    </Typography>
                </div>
            )
        }


        return <div className="results">
            {
                // loop over specification levels
                Object.keys(results[params.image_id])
                    // only get A B C sections
                    .filter(specification_level => (
                        (specification_level != "image_tag") && (specification_level != "overall_score"))
                    )
                    .filter(specification_level => (
                        (results[params.image_id][specification_level]["completed"])))
                    // A, B C instead of C, B, A
                    .reverse()
                    .map((specification_level) =>
                        <Accordion
                            className='category-accordion'
                            key={specification_level}
                            aria-label="Click to view details about this specification level analysis"
                            title={`View details about specification level ${specification_level} analysis`}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <div style={{ width: "100%", display: "flex", justifyContent: "space-between" }}>
                                    <Typography variant="h5" display="inline">
                                        {specification_level}
                                    </Typography>
                                    <Typography variant="h5" display="inline">
                                        {
                                            "Passed: " +
                                            (results[params.image_id][specification_level]["results"]["passed"] ? "Yes" : "No")
                                        }
                                    </Typography>
                                </div>
                            </AccordionSummary>
                            <AccordionDetails>
                                {
                                    generateResultsAccordion(results[params.image_id][specification_level]["results"])
                                }
                            </AccordionDetails>
                        </Accordion >
                    )
            }
        </div >
    }

    const generateResultsAccordion = (resultData) => {
        // loop over result categories
        return Object.keys(resultData)
            // not care about passed/not passed here
            .filter((result_category) => result_category != "passed")
            .map((result_category) =>
                <Accordion
                    className="result-accordion"
                    key={result_category}
                    aria-label="Click to view details about an analysis category"
                    title={`View ${result_category} details`} >
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
                </Accordion >
            )
    }

    return (
        <div className="container" >
            <div className="top-bar">
                <IconButton
                    color="primary"
                    aria-label="Return to result page"
                    component={Link}
                    to={`/results/${params.session_id}`}
                    size="large"
                    title="Go back to result overview">
                    <ArrowBackIosIcon fontSize="large" />
                </IconButton>
                <HomeButton aria-label="Button for going back to home page"></HomeButton>
                <IconButton
                    aria-label="Download button for single image"
                    size="large"
                    sx={{ color: "#1976d2" }}
                    onClick={handleDownload}
                    title="Download image">
                    <DownloadIcon fontSize='large' />
                </IconButton>
            </div>

            <Typography variant="h2">
                Resultat: {params.image_id}
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
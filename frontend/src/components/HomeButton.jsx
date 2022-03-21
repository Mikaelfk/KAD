import React from 'react'
import { Link } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import HomeIcon from '@mui/icons-material/Home';


const HomeButton = () => {
    return (
        <IconButton color="primary" aria-label="Home button" component={Link} to="/" size="large">
            <HomeIcon fontSize="large" />
        </IconButton>
    )
}

export default HomeButton;
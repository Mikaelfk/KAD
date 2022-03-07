import React from 'react';
import './MainPage.css';
import { Card, CardMedia, CardContent, Typography, Divider } from '@mui/material';
import { Link } from 'react-router-dom';



const MainPage = () => {
    return (
        <div className='container'>
            <Typography variant='h2'>Kvalitetssikring</Typography>
            <div className='image-target-menu'>
                <Card component={Link} to='/upload/object' style={{ textDecoration: 'none' }}>
                    <CardContent className='image-target-menu-option'>
                        <Typography variant="h4">Object Level Target</Typography>
                        <Divider variant="middle" sx={{ borderBottomWidth: 2, padding: '5px' }} flexItem />
                        <CardMedia
                            component="img"
                            sx={{ width: 300, padding: '15px' }}
                            image="/images/object_level_target.PNG"
                            alt="Object level target image"
                        />
                    </CardContent>
                </Card>
                <Card component={Link} to='/upload/device' style={{ textDecoration: 'none' }}>
                    <CardContent className='image-target-menu-option'>
                        <Typography variant="h4">Device Level Target</Typography>
                        <Divider variant="middle" sx={{ borderBottomWidth: 2, padding: '5px' }} flexItem />
                        <Divider />
                        <CardMedia
                            component="img"
                            sx={{ width: 200, padding: '15px' }}
                            image="/images/device_level_target.jpg"
                            alt="Device level target image"
                        />
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

export default MainPage;
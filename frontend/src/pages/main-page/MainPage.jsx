import { Card, CardContent, CardMedia, Divider, Typography } from '@mui/material';
import React from 'react';
import { Link } from 'react-router-dom';
import './MainPage.css';



const MainPage = () => {
    return (
        <div className='container'>
            <Typography variant='h2'>Kvalitetssikring</Typography>
            <div className='image-target-menu'>
                <Card component={Link} to='/upload/object' style={{ textDecoration: 'none' }}>
                    <CardContent>
                        <div className="image-target-menu-option">
                            <Typography variant="h4">Object Level Target</Typography>
                            <Divider variant="middle" sx={{ borderBottomWidth: 2, padding: '5px' }} flexItem />
                            <CardMedia
                                component="img"
                                image="/images/object_level_target.PNG"
                                alt="Object level target image"
                            />
                        </div>
                    </CardContent>
                </Card>
                <Card component={Link} to='/upload/device' style={{ textDecoration: 'none' }}>
                    <CardContent>
                        <div className='image-target-menu-option'>
                            <Typography variant="h4">Device Level Target</Typography>
                            <Divider variant="middle" sx={{ borderBottomWidth: 2, padding: '5px' }} flexItem />
                            <CardMedia
                                component="img"
                                image="/images/device_level_target.jpg"
                                alt="Device level target image"
                            />
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

export default MainPage;
import React from 'react';
import * as Constants from '../../Constants';
import classes from './Logo.css';

const logo = (props) => (
    <div className={classes.Logo} style={{height: props.height}}>
        <img src={ Constants.LOCAL_IMAGE_URL + props.src} alt="logo" />
    </div>
);

export default logo;
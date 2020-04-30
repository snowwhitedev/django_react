import React from 'react';

import classes from './Avata.css';

const avata = (props) => (
    <div className={classes.Avata} style={{height: props.height}}>
        <img src={ localStorage.getItem('user_imageUrl') } alt="avata" />
    </div>
);

export default avata;
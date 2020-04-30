import React from 'react';

import classes from './Title.css';

const title = (props) => (
    <div className={ [classes.TitleContainer, classes[props.font]].join(' ') } >
        {props.children}
    </div>
);

export default title
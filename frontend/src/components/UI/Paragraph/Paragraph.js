import React from 'react';

import classes from './Paragraph.css';

const paragraph = (props) => (
    <div className={ [classes.Paragraph, classes[props.fontWeight], classes[props.font], classes[props.margin], classes[props.color]].join(' ') } >
        {props.children}
    </div>
);

export default paragraph
import React from 'react';
import Button from '../../../components/UI/Button/Button';

import classes from './SubTitle.css';

const subtitle = (props) => (
    <div className={ classes.SubTitleContainer } >
        {props.children}
    </div>
);

export default subtitle
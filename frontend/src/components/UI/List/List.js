import React from 'react';

import classes from './List.css';
  
const lists = (props) => {

    return (
        <ul className={classes.lists} >
        {
            props.children
        }
        </ul>
    );
}

export default lists;
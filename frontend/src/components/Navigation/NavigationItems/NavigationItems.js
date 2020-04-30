import React from 'react';
import classes from './NavigationItems.css';
import * as Constants from '../../../Constants';

import NavigationItem from './NavigationItem/NavigationItem';

const navigationItems = () => {
    let navItem = "";
    if(localStorage.getItem("user_Authority") === "true") {
        navItem = (
            <NavigationItem link="/users" exact>{ Constants.PEOPLE }</NavigationItem>
        );
    }
    else{
        navItem = "";
    }
    return (
        <ul className={classes.NavigationItems}>
            <NavigationItem link="/repetition">{ Constants.REPETITION }</NavigationItem>
            <NavigationItem link="/policy" exact>{ Constants.HANDBOOK }</NavigationItem>
            { navItem }
        </ul>
    )
}

export default navigationItems;
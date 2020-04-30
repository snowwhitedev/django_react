import React from 'react';

import classes from './Toolbar.css';
import Logo from '../../Logo/Logo';
import Avata from '../../Avata/Avata';
import NavigationItems from '../NavigationItems/NavigationItems';
import mainLogo from  '../../../assets/images/main-logo.png';
import * as Constants from '../../../Constants';

const toolbar = (props) => {
    var toolbarType = '';
    if(props.pageType === "main") {
        toolbarType = (
            <header className={classes.Toolbar}>
                <div className={classes.Logo}>
                    <Logo src={ mainLogo } />
                    <h5 className={classes.logoTitle}>{ Constants.LOGOTITLE }</h5>
                </div>
                    
                <nav className={classes.DesktopOnly}>
                    <NavigationItems />
                </nav>
                <div className={classes.Avata}>
                    <Avata />
                </div>
            </header>
        );        
    }
    else if(props.pageType === "detail") {
        toolbarType = (
            <header className={classes.Toolbar}>
                <div className={classes.Logo}>
                    
                    <h5 className={classes.backTitle} onClick={ props.clicked }><span className={[classes.icon, classes.back].join(' ')}></span>{ props.tabName }</h5>
                </div>
                <div className={classes.Avata}>
                    <Avata />
                </div>
            </header>
        );        
    }

    return toolbarType;
}

export default toolbar;
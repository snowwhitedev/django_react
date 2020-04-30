import React, { Component } from 'react';

import Aux from '../Au/Auxx';
import classes from './Layout.css';
import Toolbar from '../../components/Navigation/Toolbar/Toolbar';

class Layout extends Component{
    
    render(){
        return(
            <Aux>
                <Toolbar pageType={ this.props.pageType } clicked={ this.props.clicked } tabName={ this.props.tabName } />
                <main className={classes.Content}>
                    {this.props.children}
                </main>
            </Aux>
        );
    }
} 
export default Layout;
import React, {Component} from 'react';

import Logo from '../../Logo/Logo';
import HorizontalLine from '../../UI/HorizontalLine/HorizontalLine';
import SocialLogin from '../SocialLoginSection/SocialLoginSection';
import mainLogo from  '../../../assets/images/main-logo.png';
import * as Constants from '../../../Constants';

import classes from './LoginPanel.css';

class LoginPanel extends Component{
    render(){

        return (
            <div className={classes.LoginPanel}>
                <Logo src={mainLogo} />
                <h5 className={classes.logoTitle}>{ Constants.LOGOTITLE }</h5>
                <HorizontalLine/>
                <SocialLogin responseGoogle={this.props.responseGoogle}/>
            </div>
        );
    }
} 


export default LoginPanel;
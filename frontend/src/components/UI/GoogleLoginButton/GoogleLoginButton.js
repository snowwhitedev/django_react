// require('dotenv').config();
// import 'dotenv/config';
import React from 'react';
import GoogleLogin from 'react-google-login';
import SocialLoginIcon from  '../../../assets/images/google-login-icon.png';
import * as Constants from '../../../Constants';

import classes from './GoogleLoginButton.css';

const ggbutton = (props) => (
    <GoogleLogin
        clientId={ Constants.GOOGLE_LOGIN_CLIENT_ID }
        buttonText={ Constants.GOOGLE_LOGIN_BUTTON_TEXT }
        render={renderProps => (
            <button className={ classes.ggbutton } onClick={renderProps.onClick} disabled={renderProps.disabled}><img src={ Constants.LOCAL_IMAGE_URL + SocialLoginIcon} alt="google login" /><span>{ Constants.GOOGLE_LOGIN_BUTTON_TEXT }</span></button>
          )}        
        onSuccess={props.responseGoogle}
        onFailure={props.responseGoogle} 
        cookiePolicy={'single_host_origin'}
    />
);

export default ggbutton
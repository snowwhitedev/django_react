import React from 'react';

import { withRouter } from 'react-router-dom';

import GoogleLoginButton from '../../UI/GoogleLoginButton/GoogleLoginButton';
import classes from './SocialLoginSection.css';

const SocialLoginSection = (props) => {
    return (

        <div className={classes.SocialLogin}>
            <GoogleLoginButton responseGoogle={props.responseGoogle} />
        </div>
    );
    
}


export default withRouter(SocialLoginSection);
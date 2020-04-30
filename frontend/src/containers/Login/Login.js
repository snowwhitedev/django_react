import React, {Component} from 'react';

import Aux from '../../hoc/Au/Auxx';
import LoginPanel from '../../components/Login/LoginPanel/LoginPanel';
import Modal from '../../components/UI/Modal/Modal';
import withErrorHandler from '../../hoc/WithErrorHandler/WithErrorHandler';
import { withRouter } from 'react-router-dom';
import * as Constants from '../../Constants';
import axios from '../../axios-instance';

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            logining: false,
            errorModal: false,
            errorMessage: ""
        };
    }

    modalCancelHandler = () => {
        this.setState({errorModal: false});
    }

    responseGoogle = (response) => {
        if(response && response.googleId !== null && response.googleId !== undefined) {
            const formData = {
                "email": `${response.profileObj.email}`,
                "username": `${response.profileObj.name}`,
                "first_name": `${response.profileObj.givenName}`,
                "last_name": `${response.profileObj.familyName}`,
                "gavatar": `${response.profileObj.imageUrl}`,
                "appkey": `${Constants.APP_SECRET_KEY}`
            };
            const encodeForm = (data) => {
                return Object.keys(data)
                    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
                    .join('&');
              }
            axios.post("login/", encodeForm(formData))
            .then(item => {
                let api_response = item.data;
                if(api_response.code === 200){
                    localStorage.setItem('token', api_response.token);
                    localStorage.setItem('user_id', api_response.user_id);
                    localStorage.setItem('user_imageUrl', response.profileObj.imageUrl);
                    this.setState({
                        logining: true
                    });
                    let authority = api_response.isAdmin;
                    localStorage.setItem('user_Authority', authority);
                    let repetitionState = api_response.finishedRepetition;
                    if(!repetitionState) {
                        this.props.history.push('/repetition');
                    }
                    else{
                        this.props.history.push('/policy');
                    }
                }
                else{
                    this.setState({
                        errorModal: true,
                        errorMessage: api_response.message
                    });
                }
            });
        }
        else{
            console.log(response);
            this.setState({
                errorModal: true,
                errorMessage: "Login failed"
            })
        }
    }


    render(){
        const loginPanel = (
            <LoginPanel responseGoogle={this.responseGoogle} />
        );

        return(
            <Aux>
                <Modal show={this.state.errorModal} modalClosed={this.modalCancelHandler}>
                    {this.state.errorMessage}        
                </Modal>
               {loginPanel} 
            </Aux>
        );
    }
}

export default withErrorHandler(withRouter(Login), axios);
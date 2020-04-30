import React, {Component} from 'react';

import Aux from '../../hoc/Au/Auxx';
import withErrorHandler from '../../hoc/WithErrorHandler/WithErrorHandler';
import Modal from '../../components/UI/Modal/Modal';
import axios from '../../axios-instance';
import Layout from '../../hoc/Layout/Layout';
import Userlists from '../../components/Users/UserList/UserList';
import Userdetail from '../../components/Users/UserDetail/UserDetail';

class Users extends Component {
    constructor(props) {
        super(props);
        this.state={
            token: localStorage.getItem('token'),
            initialList: [],
            userList: [],
            userDetail: "",
            pageType: "main",
            errorModal: false,
            errorMessage: ""
        } 
        
    }

    componentDidMount(){
        try {
            axios.get("people", {
                headers: {
                    'Authorization': `Token ${this.state.token}`
                }
            })
            .then(item => {
                if(item.status === 200) {
                    let api_responsive = item.data;
                    this.setState({
                        userList: api_responsive
                    })
                }
                else{
                    this.setState({
                        errorModal: true,
                        errorMessage: api_response.message
                    });
                }
            });
        } catch (e) {
            console.log("user list error", e);
            this.setState({
                errorModal: true,
                errorMessage: "People request failed" + e
            });
        }
    }

    modalCancelHandler = () => {
        this.setState({errorModal: false});
    }

    pageDetailView = (index) => {
        let user_id = this.state.userList[index].id;

        try {
            axios.get("people/documents/",
            {
                headers: {
                    'Authorization': `Token ${this.state.token}`                    
                },
                params: {user_id: user_id}
            })
            .then(item => {
                if(item.status === 200) {
                    let api_responsive = item.data;
                    this.setState({
                        initialList: api_responsive
                    });
                }
                else{
                    this.setState({
                        errorModal: true,
                        errorMessage: api_response.message
                    });
                }
            });
        } catch (e) {
            console.log("user list error", e);
            this.setState({
                errorModal: true,
                errorMessage: "People request failed" + e
            });
        }
       
        this.setState({
            userDetail: this.state.userList[index],
            pageType: "detail"
        });

    }

    pageBackView = () => {
        this.setState({
            pageType: "main"
        })
    }
    

    render(){
        let loadPage = '';

        if(this.state.pageType === "main") {
            loadPage = (
                <Userlists userList={ this.state.userList } clicked={this.pageDetailView} md={this.props.md} />
            );
        }
        else if(this.state.pageType === "detail") {
            loadPage = (
                <Userdetail initialList={ this.state.initialList } userDetail={ this.state.userDetail } md={this.props.md} />
            );
        }

        return(
            <Aux>
                <Layout pageType={ this.state.pageType } clicked={this.pageBackView} tabName={"People"}>
                    <Modal show={this.state.errorModal} modalClosed={this.modalCancelHandler}>
                        {this.state.errorMessage}        
                    </Modal>
                    { loadPage }
                </Layout>
            </Aux>
        );
    }
}

export default withErrorHandler(Users, axios);
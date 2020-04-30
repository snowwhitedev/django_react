import React, {Component} from 'react';

import Aux from '../../hoc/Au/Auxx';
import withErrorHandler from '../../hoc/WithErrorHandler/WithErrorHandler';
import Modal from '../../components/UI/Modal/Modal';
import axios from '../../axios-instance';
import Layout from '../../hoc/Layout/Layout';
import Policylists from '../../components/Policy/PolicyList/PolicyList';
import Policydetail from '../../components/Policy/PolicyDetail/PolicyDetail';
import * as Constants from '../../Constants';


class Policy extends Component {
    constructor(props) {
        super(props);
        this.state={
            initialList: [],
            token: localStorage.getItem('token'),
            pageType: "main",
            policyDetail: [],
            documentId: 0,
            errorModal: false,
            errorMessage: ""
        } 
    }


    modalCancelHandler = () => {
        this.setState({errorModal: false});
    }


    componentDidMount(){
        try {
            axios.get("handbook", {
                headers: {
                    'Authorization': `Token ${this.state.token}`
                }
            })
            .then(item => {
                if(item.status === 200) {
                    let handbookList = item.data;
                    handbookList.map((res, index) => {
                        res.duedate = Constants.convert_date(res.dueon);
                        this.setState(state => {
                            const initialList = [ ...state.initialList, res];
                            return {
                                initialList,
                            }
                        });
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
            console.log("error", e);
            this.setState({
                errorModal: true,
                errorMessage: "Handbook request failed" + e
            });
        }
    }

    checkedChange = (question_index, index) => {
        let questionItem = {
            ...this.state.policyDetail[0].questions[question_index].policyGroup[index]
        }
        
        let itemState = questionItem.finished;
        let itemId = questionItem.id;
        let requestUrl = "handbook/policies/" + itemId + "/";
        if(!itemState){
            try {
                axios.put(requestUrl, {}, {
                    headers: {
                        'Authorization': `Token ${this.state.token}`
                    }
                })
                .then(item => {
                    console.log("item status first", item);
                    if(item.status === 200 && item.data.message === "checked") {
                        questionItem.finished = !itemState;

                        let policyDetailList = [ ...this.state.policyDetail[0].questions ];

                        policyDetailList[question_index].policyGroup[index] = questionItem;
                
                        let policyDetailItem = { ...this.state.policyDetail[0] };
                
                        policyDetailItem.questions = policyDetailList;
                
                        let policyDetail = [ ...this.state.policyDetail ];
                
                        policyDetail[0] = policyDetailItem;
                
                        this.setState({ policyDetail: policyDetail });        
                    }
                    else {
                        console.log("policy item checked error", e);
                        this.setState({
                            errorModal: true,
                            errorMessage: api_response.message
                        });
                    }
                });
            } catch (e) {
                console.log("policy item checked error", e);
                this.setState({
                    errorModal: true,
                    errorMessage: "Handbook policy item request failed: " + e
                });
            }
    
        }
    }

    pageDetailView = (id) => {
        let initialIndex = this.state.initialList.findIndex(res => {
            return res.document__id === id
        });

        let policyDetailItem = {
            ...this.state.policyDetail[0]
        }

        try {
            axios.get("handbook/policies/", {
                headers: {
                    'Authorization': `Token ${this.state.token}`,
                    'DocumentId': `${id}`
                }
            })
            .then(item => {
                if(item.status === 200) {
                    policyDetailItem.questions = item.data;
                }
                else{
                    policyDetailItem.questions = [];
                }
                policyDetailItem.title = this.state.initialList[initialIndex].document__title;
                policyDetailItem.duedate = this.state.initialList[initialIndex].duedate;
                policyDetailItem.overdue = this.state.initialList[initialIndex].overdue;
                policyDetailItem.description = this.state.initialList[initialIndex].document__description;
                let policyDetail = [ ...this.state.policyDetail ];

                policyDetail[0] = policyDetailItem;

                this.setState({ 
                    policyDetail: policyDetail,
                    pageType: "detail",
                    documentId: id
                });        
            });
        } catch (e) {
            policyDetailItem.questions = [];
            console.log("policy item error", e);
            this.setState({
                errorModal: true,
                errorMessage: "Policy item request failed" + e
            });
        }
    }

    pageBackView = () => {
        let policyDetailItem = this.state.policyDetail[0].questions;
        let policyStateBoolean = false;
        let policyDetailState = policyDetailItem.map(res => {
            let policyState = res.policyGroup.find(item => item.finished == false);
            if(policyState !== undefined){
                policyStateBoolean = true;
                return policyStateBoolean;
            }
        });
        if(!policyStateBoolean){
            let initialIndex = this.state.initialList.findIndex(item => {
                return item.document__id === this.state.documentId
            });
            let initialListItem = {
                ...this.state.initialList[initialIndex]
            };
            initialListItem.finished = true;
            let initialList = [
                ...this.state.initialList
            ];
            initialList[initialIndex] = initialListItem;
            this.setState({
                initialList: initialList
            });
        }
        this.setState({
            pageType: "main"
        })
    }
    

    render(){
        let loadPage = '';

        if(this.state.pageType === "main") {
            loadPage = (
                <Policylists initialList={ this.state.initialList } clicked={this.pageDetailView} md={this.props.md} />
            );
        }
        else if(this.state.pageType === "detail") {
            loadPage = (
                <Policydetail policyDetail={ this.state.policyDetail } clicked={this.checkedChange} md={this.props.md} />
            );
        }
        return(
            <Aux>
                <Layout pageType={ this.state.pageType } clicked={this.pageBackView} tabName={"Handbook"}>
                    <Modal show={this.state.errorModal} modalClosed={this.modalCancelHandler}>
                        {this.state.errorMessage}        
                    </Modal>
                    { loadPage }
                </Layout>
            </Aux>
        );
    }
}

export default withErrorHandler(Policy, axios);
import React, {Component} from 'react';

import Aux from '../../hoc/Au/Auxx';
import withErrorHandler from '../../hoc/WithErrorHandler/WithErrorHandler';
import Modal from '../../components/UI/Modal/Modal';
import axios from '../../axios-instance';
import Layout from '../../hoc/Layout/Layout';
import RepetitionQuestion from '../../components/Repetition/RepetitionQuestion/RepetitionQuestion';
import RepetitionAnswer from '../../components/Repetition/RepetitionAnswer/RepetitionAnswer';
import RepetitionEmpty from '../../components/Repetition/RepetitionEmpty/RepetitionEmpty';
import SubHeader from '../../components/UI/SubHeader/SubHeader';
import * as Constants from '../../Constants';

class Repetition extends Component {
    constructor(props) {
        super(props);
        this.state={
            token: localStorage.getItem('token'),
            initialList: [],
            totalNumber: 0,
            passNumber:0,
            dueon:'',
            overdue: false,
            pageType: "main",
            pageState: "",
            answerNumber: -1,
            errorModal: false,
            errorMessage: ""
        } 
        
    }

    componentDidMount(){
        try {
            axios.get("repetition", {
                headers: {
                    'Authorization': `Token ${this.state.token}`
                }
            })
            .then(item => {
                if(item.status === 200) {

                    let api_response = item.data;
                    let currentDate = new Date();
                    let dueon = Constants.convert_date(api_response.dueon);
                    let overdue = false;
                    this.setState({
                        totalNumber: api_response.total,
                        passNumber: api_response.passed,
                        initialList: api_response.data,
                        dueon: dueon,
                        overdue: api_response.overdue
                    }, function(){
                        if(this.state.totalNumber !== this.state.passNumber){
                            this.setState({
                                pageState: "question"
                            });
                        }
                        else{
                            this.setState({
                                pageState: "empty"
                            });
                        }
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
        }
    }

    modalCancelHandler = () => {
        this.setState({errorModal: false});
    }

    AnswerView = (index) => {
        this.setState({
            pageState: "answer"
        })
    }

    AnswerViewKeypress = (event) => {
        if(event.key === "Enter") {
            this.setState({
                pageState: "answer"
            })
        }
    }

    AnswerRegister = (index, answerValue) => {
        if(index < this.state.totalNumber - this.state.passNumber - 1) {
            let initialListItem = { 
                ...this.state.initialList[index + 1]
            }

            let questionId = initialListItem.id;
            try {
                axios.put("repetition/" + questionId + '/', { answer: answerValue},
                {
                    headers: {
                        'Authorization': `Token ${this.state.token}`
                    }
                })
                .then(item => {
                    if(item.status === 200) {
                        initialListItem.answer = answerValue;
    
                        let initialList = [
                            ...this.state.initialList
                        ]
                
                        initialList[index + 1] = initialListItem;
                
                        let answerNumber = index + 1;
                
                        if(answerNumber < (this.state.totalNumber - this.state.passNumber - 1)){
                            this.setState({
                                initialList: initialList,
                                pageState: "question",
                                answerNumber: answerNumber
                            });          
                        }
                        else{
                            this.setState({
                                initialList: [],
                                pageState: "empty",
                                answerNumber: -1
                            });
                        }
                    }
                    else{
                        console.log("answer register", item);
                        this.setState({
                            errorModal: true,
                            errorMessage: "Answer register failed"
                        });
                    }
                });
            } catch (e) {
                console.log("answer register error", e);
                this.setState({
                    errorModal: true,
                    errorMessage: "Answer register request failed" + e
                });
            }

    
        }
        else{
            this.setState({
                initialList: [],
                pageState: "empty",
                answerNumber: -1
            });
        }
    }
    

    
    render(){
        let loadPage = '';
        let loadSubHeader = '';

        if(this.state.pageState === "question") {
            loadPage = (                
                <RepetitionQuestion question={ this.state.initialList[this.state.answerNumber + 1] } AnswerNumber={ this.state.answerNumber } keypress={ this.AnswerViewKeypress } clicked={ this.AnswerView } md={this.props.md} />
            );
            loadSubHeader = (
                <SubHeader AnswerNumber={ this.state.answerNumber } dueon={ this.state.dueon } overdue={ this.state.overdue } totalNumber={this.state.totalNumber} passed={this.state.passNumber} />
            );
        }
        else if(this.state.pageState === "answer") {
            loadSubHeader = (
                <SubHeader AnswerNumber={ this.state.answerNumber } dueon={ this.state.dueon }  overdue={ this.state.overdue } totalNumber={this.state.totalNumber} passed={this.state.passNumber} />
            );
            loadPage = (
                <RepetitionAnswer question={ this.state.initialList[this.state.answerNumber + 1] }  AnswerNumber={ this.state.answerNumber } clicked={ this.AnswerRegister }  md={this.props.md} />
            );
        }
        else if(this.state.pageState === "empty") {
            loadSubHeader = "";
            loadPage = (
                <RepetitionEmpty />
            );
        }
       

        return(
            <Aux>
                <Layout pageType={ this.state.pageType } clicked={this.pageBackView} tabName={"Handbook"}>
                    <Modal show={this.state.errorModal} modalClosed={this.modalCancelHandler}>
                        {this.state.errorMessage}        
                    </Modal>
                    { loadSubHeader }
                    { loadPage }
                </Layout>
            </Aux>
        );
    }
}

export default withErrorHandler(Repetition, axios);
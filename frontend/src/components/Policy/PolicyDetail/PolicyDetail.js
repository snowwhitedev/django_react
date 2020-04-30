import React from 'react';

import Title from '../../UI/Title/Title';
import SubTitle from '../../UI/SubTitle/SubTitle';
import Paragraph from '../../UI/Paragraph/Paragraph';
import List from '../../UI/List/List';
import Button from '../../UI/Button/Button';
import round_checked_icon from  '../../../assets/images/round_checked.png';
import round_unchecked_icon from  '../../../assets/images/round_unchecked.png';
import * as Constants from '../../../Constants';

import classes from './PolicyDetail.css';


const policydetail = (props) => {
    return (
        <div className={classes.PolicyDetail} >
            <Title font={"font24"}>{ props.policyDetail[0].title }</Title>
            <SubTitle>
                { props.policyDetail[0].duedate }
                {(!props.policyDetail[0].overdue) ? "" : <Button btnType={"Orange"}> {"OVERDUE"} </Button>}
    
            </SubTitle>
            {
                props.policyDetail[0].questions.map((res, question_index) => {
                    return (
                        <div key={question_index}>
                            <Paragraph fontWeight={"fontWeight400"} ><p dangerouslySetInnerHTML={{__html: props.md.render(res.description) }} /></Paragraph>
                            <List listClass={ "detaillistitem" }>
                                {
                                    res.policyGroup.map((item, index) => (
                                        <li className={ classes.listitem } key={ index } onClick={props.clicked.bind(this, question_index, index)} >
                                            <img src={ item.finished ? Constants.LOCAL_IMAGE_URL + round_checked_icon : Constants.LOCAL_IMAGE_URL + round_unchecked_icon } alt='checked' />
                                            <div className={ classes.itemdiv }>
                                                <span className={ [classes.fontWeight400, classes.tableStyle].join(" ") }><p dangerouslySetInnerHTML={{__html: props.md.render(item.itemText) }} /></span>
                                            </div>
                                        </li>
                                    ))
                                }
                            </List>
                        </div>
                    )
                })
            }
        </div>
    );
}


export default policydetail;
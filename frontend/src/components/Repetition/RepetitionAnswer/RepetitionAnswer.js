import React from 'react';
import * as Constants from '../../../Constants';

import Paragraph from '../../UI/Paragraph/Paragraph'
import Button from '../../UI/Button/Button';
import HorizontalLine from '../../UI/HorizontalLine/HorizontalLine';
import classes from './RepetitionAnswer.css';



const repetitionanswer = (props) => (
    <div className={classes.RepetitionAnswer_1} >
        <div className={classes.RepetitionAnswer_2} >
            <div className={classes.RepetitionAnswer_3} >
                <Paragraph color={"colorgrey"} font={"font18"} fontWeight={"fontWeight500"} margin={"marginTopBottom1"} ><p dangerouslySetInnerHTML={{__html: props.md.render(props.question.question) }} /></Paragraph>
                <Paragraph font={"font18"} margin={"marginBottom2"} fontWeight={"fontWeight500"} ><p dangerouslySetInnerHTML={{__html: props.md.render(props.question.questionAns) }} /></Paragraph>
                <HorizontalLine />
                <Paragraph color={"colorgrey"} font={"font18"} fontWeight={"fontWeight500"} margin={"marginTopBottom1"}>{ Constants.ANSWERBUTTONTOP }</Paragraph>
                <div className={classes.RepetitionBtnGroup}>
                    <Button btnType={"Outline"} clicked={props.clicked.bind(this, props.AnswerNumber, Constants.ANSWER_VALUE_FOR_RECALL)}> { Constants.RECALL } </Button>
                    <Button btnType={"Outline"} clicked={props.clicked.bind(this, props.AnswerNumber, Constants.ANSWER_VALUE_FOR_MOREORLESS)} > { Constants.MOREORLESS } </Button>
                    <Button btnType={"Outline"} clicked={props.clicked.bind(this, props.AnswerNumber, Constants.ANSWER_VALUE_FOR_PERFECTLY)} > { Constants.PERFECTLY } </Button>
                </div>
                <Paragraph color={"colorgrey"} font={"font16"} fontWeight={"fontWeight300"} margin={"marginTopBottom1"}>{ Constants.ANSWERBUTTONBOTTOM }</Paragraph>
            </div>
        </div>
    </div>
);

export default repetitionanswer;
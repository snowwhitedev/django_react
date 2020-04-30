import React, { useEffect } from 'react';

import Paragraph from '../../UI/Paragraph/Paragraph'
import Button from '../../UI/Button/Button';
import HorizontalLine from '../../UI/HorizontalLine/HorizontalLine';
import * as Constants from '../../../Constants';
import classes from './RepetitionQuestion.css';



const repetitionquestion = (props) => {
    useEffect(() => {
        document.addEventListener('keydown', props.keypress);
    }, []);
    return (
        <div className={classes.RepetitionQuestion_1} onKeyPress={props.keypress} tabIndex={0}>
            <div className={classes.RepetitionQuestion_2} onKeyPress={props.keypress}>
                <div className={classes.RepetitionQuestion_3} onKeyPress={props.keypress}>
                    <Paragraph font={"font18"} margin={"marginBottom1"} ><p dangerouslySetInnerHTML={{__html:  props.md.render(props.question.question) }} /></Paragraph>
                    <HorizontalLine />
                    <Button btnType={"Outline"} clicked={props.clicked.bind(this, props.AnswerNumber)}> { Constants.REVEALANSWER }</Button>
                    <Button btnType={"Transparent"} color={"colorgrey"} font={"font16"} > { Constants.HITREVEAL } </Button>
                </div>
            </div>
        </div>
    );
}

export default repetitionquestion;
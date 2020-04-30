import React from 'react';

import Button from '../../../components/UI/Button/Button';
import CircularProgressbar from '../../../components/UI/CircularProgress/CircularProgressbar';
import classes from './SubHeader.css';

const subheader = (props) => (
    <div className={ classes.SubHeader } >
        <div className={ classes.SubHeaderItemLeft }>
            <CircularProgressbar sqSize={ 30 } strokeWidth={5} percentage={ (((props.passed + props.AnswerNumber + 1) / props.totalNumber) * 100) } />
            <span>{ props.passed + props.AnswerNumber + 1 } of {props.totalNumber} repeated</span>
        </div>
        <div className={ classes.SubHeaderItemRight }>
            <span>
                { props.dueon }
            </span>
            <span> { (props.overdue) ? <Button btnType={"Orange"}> {"OVERDUE"} </Button> : "" } </span>
        </div>
    </div>
);

export default subheader
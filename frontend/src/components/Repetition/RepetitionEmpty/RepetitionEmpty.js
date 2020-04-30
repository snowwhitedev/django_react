import React from 'react';

import Logo from '../../Logo/Logo';
import Paragraph from '../../UI/Paragraph/Paragraph';
import mainlogo_grey from  '../../../assets/images/main-logo-grey.png';
import * as Constants from '../../../Constants';

import classes from './RepetitionEmpty.css';



const repetitionempty = (props) => (
    <div className={classes.RepetitionEmpty} >
        <Logo src={ mainlogo_grey } />
        <div className={classes.RepetitionsParagraph} >
            <Paragraph font={"font20"} margin={"marginBottom1"}>{ Constants.ALLREPEATED }</Paragraph>
            <Paragraph font={"fontlight"} margin={"marginBottom1"}>{ Constants.ALLREPEATEDSUBTEXT }</Paragraph>
        </div>
    </div>
);

export default repetitionempty;
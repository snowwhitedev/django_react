import React from 'react';

import List from '../../UI/List/List';
import Button from '../../../components/UI/Button/Button';
import checked_icon from  '../../../assets/images/checked.png';
import unchecked_icon from  '../../../assets/images/unchecked.png';
import * as Constants from '../../../Constants';

import classes from './PolicyList.css';



const policylists = (props) => (
    <div className={classes.PolicyLists} >
        <List listClass={"policylists"}>
            {
                props.initialList.map((item, index) => (
                    <li className={ classes.listitem } key={ item.document__id }  onClick={props.clicked.bind(this, item.document__id)}>
                        <img src={ item.finished ? Constants.LOCAL_IMAGE_URL + checked_icon : Constants.LOCAL_IMAGE_URL + unchecked_icon } alt='checked' />
                        <div className={item.finished ? [classes.itemdiv, classes.checkedItem].join(' ') : classes.itemdiv}>
                            <span>{ item.document__title }</span>
                            <span>{ item.finished ? '' : item.duedate }{ (!item.finished && item.overdue) ? <Button btnType={"Orange"}> {"OVERDUE"} </Button> : "" }</span>
                        </div>
                    </li>
                ))
            }
        </List>
        {/* <List listType={ "policy_main" } policylists={props.initialList} clicked={props.clicked} /> */}
    </div>
);

export default policylists;
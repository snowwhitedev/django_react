import React from 'react';

import List from '../../UI/List/List'

import Button from '../../../components/UI/Button/Button';
import checked_icon from  '../../../assets/images/checked.png';
import unchecked_icon from  '../../../assets/images/unchecked.png';
import gavatar_icon from  '../../../assets/images/gavatar.png';
import * as Constants from '../../../Constants';

import classes from './UserDetail.css';



const userdetail = (props) => (
    <div className={classes.UserDetail} >
        <List>
            <li className={classes.userDetail}>
                <div className={ classes.userDetailInfo }><span className={ classes.userName }>{ props.userDetail.first_name + ' ' + props.userDetail.last_name }</span><span className={ classes.fontGrey }> {props.userDetail.email}</span></div>
                <img className={ classes.avataImage } src={ (props.userDetail.gavatar) ? props.userDetail.gavatar: Constants.LOCAL_IMAGE_URL + gavatar_icon } alt='user avata' />
            </li>
            {
                props.initialList.map((item, index) => (
                    <li className={ classes.listitem } key={ item.document__id } >
                        <img src={ item.finished ? Constants.LOCAL_IMAGE_URL + checked_icon : Constants.LOCAL_IMAGE_URL + unchecked_icon } alt='checked' />
                        <div className={item.finished ? [classes.itemdiv, classes.checkedItem].join(' ') : classes.itemdiv}>
                            <span>{ item.document__title }</span>
                            <span>{ item.finished ? '' : Constants.convert_date(item.dueon) }{ (!item.finished && item.overdue) ? <Button btnType={"Orange"}> {"OVERDUE"} </Button> : "" }</span>
                        </div>
                    </li>
                ))
            }
        </List>
        {/* <List listType={ "user_detail" } initiallists={ props.initialList } userDetail={ props.userDetail } /> */}
    </div>
);

export default userdetail;
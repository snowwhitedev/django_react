import React from 'react';

import List from '../../UI/List/List'
import Button from '../../../components/UI/Button/Button';
import user_checked_icon from  '../../../assets/images/user_checked.png';
import gavatar_icon from  '../../../assets/images/gavatar.png';
import * as Constants from '../../../Constants';

import classes from './UserList.css';



const userlists = (props) => (
    <div className={classes.UserLists} >
        <List listClass={"userMain"}>
            {
                props.userList.map((item, index) => (
                    <li className={ [classes.listitem, classes.userMain].join(' ') } key={ item.id }  onClick={props.clicked.bind(this, index)}>
                        <img className={classes.avataImage} src={ (item.gavatar) ? item.gavatar: Constants.LOCAL_IMAGE_URL + gavatar_icon } alt='user avata' />
                        <img src={ item.status ? Constants.LOCAL_IMAGE_URL + user_checked_icon : "" } className={item.status ? classes.checked_icon : classes.unchecked_icon} />
                        <div className={item.status ? [classes.itemdiv, classes.checkedItem].join(' ') : classes.itemdiv}>
                            <span className={ classes.Flex }><span className={ classes.userName }>{ item.first_name + ' ' + item.last_name }</span> <span className={ classes.fontGrey }> {item.email}</span></span>
                            <span className={ classes.fontGrey }>{ item.status ? '' : Constants.convert_date(item.dueon) }{ (!item.status && item.overDue) ? <Button btnType={"Orange"}> {"OVERDUE"} </Button> : "" }</span>
                        </div>
                    </li>
                ))
            }
        </List>
        {/* <List listType={ "user_main" } userlists={ props.userList } clicked={props.clicked} /> */}
    </div>
);

export default userlists;
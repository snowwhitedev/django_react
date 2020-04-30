import React, {Component} from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';

import Login from './containers/Login/Login';
import Policy from './containers/Policy/Policy';
import Repetition from './containers/Repetition/Repetition';
import Users from './containers/Users/Users';
import classes from './App.css';

var isAuthenticated = false;
class App extends Component {
  constructor(props) {
    super(props);

  }

  isAuthenticated = () => {
    isAuthenticated = true;
  }

  unAuthenticated = () => {
    isAuthenticated = false;
 }

  
  
  render() {
    const PrivateRoute = ({ component: Component, ...rest }) => {
      if(localStorage.getItem("token") !== null && localStorage.getItem("token") !== undefined && localStorage.getItem("token") !== ""){
        this.isAuthenticated();
      }
      return (
        <Route {...rest} render={(props) => (
          isAuthenticated === true
            ? <Component {...props}  md={this.props.md}/>
            : <Redirect to={{
                pathname: '/'
              }} />
        )} />
      )
    }

    return (
      <div className={classes.App}>
          <Switch>
            <PrivateRoute path="/policy" component={Policy}/>
            <PrivateRoute path="/repetition" component={Repetition} />
            <PrivateRoute path="/users" component={Users} />
            <Route path="/" exact component={Login} />
          </Switch>
      </div>
    );
  }
}


export default App;


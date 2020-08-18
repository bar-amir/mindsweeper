import React from 'react';
import './App.scss';
import Home from './Home';
import Header from './Header';
import Head from './Head';
import Users from './Users';
import {
  Switch,
  Route,
  withRouter
} from "react-router-dom";

function App(props) {
  return (
    <div>
      <Head />
      {
        props.location.pathname.includes('snapshot') ? null : <Header />
      }
      <Switch>
        <Route path="/users">
          <Users />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </div>
  );
}

export default withRouter(App);

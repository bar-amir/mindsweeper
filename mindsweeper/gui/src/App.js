import React from 'react';
import './App.scss';
import Home from './Home';
import Users from './Users';
import {
  // BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

function App() {
  return (
    <div>
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

export default App;

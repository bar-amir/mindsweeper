import React from 'react';
import Sweep from './Sweep';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function User() {
  let match = useRouteMatch();
  let { userId } = useParams();

  return (
    <div>
      <Switch>
        <Route path={`${match.path}/sweeps/:sweepId`}>
          <Sweep />
        </Route>
        <Route path={match.path}>
          <h3>Requested user ID: {userId}</h3>
          <h3>Please select a Sweep.</h3>
        </Route>
      </Switch>
    </div>
  );
}

export default User;

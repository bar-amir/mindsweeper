import React from 'react';
import Snapshot from './Snapshot';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function Sweep() {
  let match = useRouteMatch();
  let { userId, sweepId } = useParams();

  return (
    <div>
      <Switch>
        <Route path={`${match.path}/snapshots/:snapshotId`}>
          <Snapshot />
        </Route>
        <Route path={match.path}>
          <h3>Requested user ID: {userId}</h3>
          <h3>Requested sweep ID: {sweepId}</h3>
        </Route>
      </Switch>
    </div>
  );
}

export default Sweep;

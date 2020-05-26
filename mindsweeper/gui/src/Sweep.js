import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
  const [snapshots, setSnapshots] = useState([]);
  
  useEffect(async () => {
    const result = await axios(
      `http://localhost:5000/users/${userId}/sweeps/${sweepId}/snapshots`,
    );
 
    setSnapshots(result.data);
  }, []);

  return (
    <div>
      <Switch>
        <Route path={`${match.path}/snapshots/:snapshotId`}>
          <Snapshot />
        </Route>
        <Route path={match.path}>
          <h3>Requested user ID: {userId}</h3>
          <h3>Requested sweep ID: {sweepId}</h3>
          <h3>Please select a Snapshot.</h3>
          <ul>
            {snapshots.map(snapshot => (
              <li key={snapshot.sweepId}>
                {snapshot.snapshotId}
              </li>
            ))}
          </ul>
        </Route>
      </Switch>
    </div>
  );
}

export default Sweep;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
  const [sweeps, setSweeps] = useState([]);
  
  useEffect(async () => {
    const result = await axios(
      `http://localhost:5000/users/${userId}/sweeps`,
    );
 
    setSweeps(result.data);
  }, []);

  return (
    <div>
      <Switch>
        <Route path={`${match.path}/sweeps/:sweepId`}>
          <Sweep />
        </Route>
        <Route path={match.path}>
          <h3>Requested user ID: {userId}</h3>
          <h3>Please select a Sweep.</h3>
          <ul>
            {sweeps.map(sweep => (
              <li key={sweep.sweepId}>
                {sweep.sweepId}
              </li>
            ))}
          </ul>
        </Route>
      </Switch>
    </div>
  );
}

export default User;

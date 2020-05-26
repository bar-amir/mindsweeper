import React, { useState, useEffect } from 'react';
import axios from 'axios';
import User from './User';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function Users() {
  let match = useRouteMatch();
  const [users, setUsers] = useState([]);
  
  useEffect(async () => {
    const result = await axios(
      'http://localhost:5000/users',
    );
 
    setUsers(result.data);
  }, []);

  return (
    <div>
      <Switch>
        <Route path={`${match.path}/:userId`}>
          <User />
        </Route>
        <Route path={match.path}>
          <h3>Please select a user.</h3>
          <ul>
            {users.map(user => (
              <li key={user.userId}>
                {user.username}
              </li>
            ))}
          </ul>
        </Route>
      </Switch>
    </div>
  );
}

export default Users;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import User from './User';
import {
  Switch,
  Route,
  Link,
  useRouteMatch,
} from "react-router-dom";

function Users() {
  let match = useRouteMatch();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      const res = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users`, { timeout: 5000 }
      )
      .then(function (response) {
        setUsers(response.data);
      })
      .catch(function (error) {
        console.log(error);
        setUsers(null);
      });
      setIsLoading(false)
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (<div className="bg"></div>);
  }
  else {
    return (
      <Switch>
        <Route path={`${match.path}/:userId`}>
          <User />
        </Route>
        <Route path={match.path}>
          {users ? 
            <table className="double">
              <thead>
                <tr>
                  <th>Test subject number</th>
                  <th>Test subject name</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.userId}>
                    <td><Link title={user.username} to={`/users/${user.userId}`}>№ {user.userId}</Link></td>
                    <td><Link title={user.username} to={`/users/${user.userId}`}>{user.username}</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          : <div class="wrapper">No test subjects to show.</div> }
        </Route>
      </Switch>
    );
  }
}

export default Users;

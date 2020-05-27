import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Head from './Head';
import Header from './Header';
import User from './User';
import Loading from './Loading';
import {
  Switch,
  Route,
  Link,
  useRouteMatch,
} from "react-router-dom";
import { Table, Breadcrumb } from 'react-bootstrap';

function Users() {
  let match = useRouteMatch();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      const result = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users`,
      );
      setUsers(result.data);
      setIsLoading(false)
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (<div><Head /><Loading /></div>);
  }
  else {
    return (
      <div>
        <Switch>
          <Route path={`${match.path}/:userId`}>
            <User />
          </Route>
          <Route path={match.path}>
            <Head />
            <Header variant="light" />
            <Breadcrumb className="m-3">
              <Breadcrumb.Item active>Users</Breadcrumb.Item>
            </Breadcrumb>
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.userId}>
                    <td>{user.userId}</td>
                    <td><Link title={user.username} to={`/users/${user.userId}`}>{user.username}</Link></td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Route>
        </Switch>
      </div>
    );
  }
}

export default Users;

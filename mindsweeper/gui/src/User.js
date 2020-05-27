import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Head from './Head';
import Header from './Header';
import Loading from './Loading';
import Sweep from './Sweep';
import {
  // BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
} from "react-router-dom";
import { Table, Breadcrumb } from 'react-bootstrap';

function User(props) {
  let match = useRouteMatch();
  let { userId } = useParams();
  const [user, setUser] = useState([]);
  const [sweeps, setSweeps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      const result_user = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}`,
      )
      const result_sweeps = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps`,
      );
      setUser(result_user.data);
      setSweeps(result_sweeps.data);
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
          <Route path={`${match.path}/sweeps/:sweepId`}>
            <Sweep user={user} />
          </Route>
          <Route path={match.path}>
            <Head />
            <Header variant="light" />
            <Breadcrumb className="m-3">
              <Breadcrumb.Item><Link title="Users" to="/users">Users</Link></Breadcrumb.Item>
              <Breadcrumb.Item active>{user.username}</Breadcrumb.Item>
            </Breadcrumb>
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Date taken</th>
                  <th>Snapshots Count</th>
                </tr>
              </thead>
              <tbody>
                {sweeps.map((sweep, index) => (
                  <tr key={sweep.sweepId}>
                    <td>{index + 1}</td>
                    <td><Link title="Sweep" to={`${user.userId}/sweeps/${sweep.sweepId}`}>{sweep.start}</Link></td>
                    <td>{sweep.numOfSnapshots}</td>
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

export default User;

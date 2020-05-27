import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Head from './Head';
import Header from './Header';
import Loading from './Loading';
import Snapshot from './Snapshot';
import {
  // BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";
import { Table, Breadcrumb } from 'react-bootstrap';

function Sweep(props) {
  let match = useRouteMatch();
  let { userId, sweepId } = useParams();
  const [sweep, setSweep] = useState([]);
  const [snapshots, setSnapshots] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  var body = <Loading />

  useEffect(() => {
    async function fetchData() {
      const res_sweep = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps/${sweepId}`,
      );
      setSweep(res_sweep.data);
      const res_snapshots = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps/${sweepId}/snapshots`,
      );
      setSnapshots(res_snapshots.data);
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
          <Route path={`${match.path}/snapshots/:snapshotId`}>
            <Snapshot key={window.location.pathname} snapshots={snapshots} user={props.user} sweep={sweep}/>
          </Route>
          <Route path={match.path}>
            <Head />
            <Header />
            <Breadcrumb className="m-3">
              <Breadcrumb.Item><Link to="/users">Users</Link></Breadcrumb.Item>
              <Breadcrumb.Item><Link to={`/users/${props.user.userId}`}>{props.user.username}</Link></Breadcrumb.Item>
              <Breadcrumb.Item href="#" active>Sweep</Breadcrumb.Item>
            </Breadcrumb>
            <div>
                <Table striped bordered hover>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Date taken</th>
                    </tr>
                  </thead>
                  <tbody>
                    {snapshots.map((snapshot, index) => (
                      <tr key={snapshot.snapshotId}>
                        <td>{index + 1}</td>
                        <td><Link to={`${sweepId}/snapshots/${snapshot.snapshotId}`}>{snapshot.datetime}</Link></td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
          </Route>
        </Switch>
      </div>
    );
  }
}

export default Sweep;

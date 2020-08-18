import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Snapshot from './Snapshot';
import {
  // BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function Sweep(props) {
  let match = useRouteMatch();
  let { userId, sweepId } = useParams();
  const [sweep, setSweep] = useState([]);
  const [user, setUser] = useState([]);
  const [snapshots, setSnapshots] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const res_user = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}`,
      );
      setUser(res_user.data);

      const res_sweep = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps/${sweepId}`,
      );
      setSweep(res_sweep.data);

      const res_snapshots = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps/${sweepId}/snapshots`,
      )
      .then(function (response) {
        setSnapshots(response.data);
      })
      .catch(function (error) {
        console.log(error);
        setSnapshots(null);
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
        <Route path={`${match.path}/snapshots/:snapshotId`}>
          <Snapshot key={window.location.pathname} snapshots={snapshots} user={props.user} sweep={sweep}/>
        </Route>
        <Route path={match.path}>
          <div className="details">
          <div className="table-row">
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Sweep name</div>
                <div className="table-block-data">{sweep.name}</div>
              </div>
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
            </div>
            <div className="table-row mt">
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Start date</div>
                <div className="table-block-data">{sweep.startDate}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Start time</div>
                <div className="table-block-data">{sweep.startTime}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Test subject</div>
                <div className="table-block-data"><Link title={user.username} to={`/users/${user.userId}`}>{user.username}</Link></div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Duration</div>
                <div className="table-block-data">{sweep.duration}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Snapshot count</div>
                <div className="table-block-data">{sweep.numOfSnapshots}</div>
              </div>
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
            </div>
          </div>
          {snapshots ? 
            <table className="double">
              <thead>
                <tr>
                  <th>Snapshot number</th>
                  <th>Snapshot timestamp</th>
                </tr>
              </thead>
              <tbody>
                {snapshots.map((snapshot, index) => (
                  <tr id={snapshot.snapshotId} key={snapshot.snapshotId}>
                    <td><Link title="Snapshot" to={`${sweepId}/snapshots/${snapshot.snapshotId}`}>№ {index + 1}</Link></td>
                    <td><Link title="Snapshot" to={`${sweepId}/snapshots/${snapshot.snapshotId}`}>{snapshot.datetime}</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          : <div class="wrapper">No snapshots to show.</div> }
        </Route>
      </Switch>
    );
  }
}

export default Sweep;

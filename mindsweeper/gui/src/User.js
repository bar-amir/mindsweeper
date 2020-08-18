import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sweep from './Sweep';
import {
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
} from "react-router-dom";

function User(props) {
  let match = useRouteMatch();
  let { userId } = useParams();
  const [user, setUser] = useState([]);
  const [sweeps, setSweeps] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      const res_user = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}`,
      );
      setUser(res_user.data);
      
      const res_sweeps = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/sweeps`,
      )
      .then(function (response) {
        setSweeps(response.data);
      })
      .catch(function (error) {
        console.log(error);
        setSweeps(null);
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
        <Route path={`${match.path}/sweeps/:sweepId`}>
          <Sweep user={user} />
        </Route>
        <Route path={match.path}>
          <div className="details">
            <div className="table-row">
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Test subject number</div>
                <div className="table-block-data">№ {user.userId}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Test subject name</div>
                <div className="table-block-data">{user.username}</div>
              </div>
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
            </div>
            <div className="table-row">
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Birthdate</div>
                <div className="table-block-data">{user.birthday}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Gender</div>
                <div className="table-block-data">{user.gender}</div>
              </div>
              <div className="table-block space">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
              <div className="table-block">
                <div className="table-block-head">Number of sweeps</div>
                <div className="table-block-data">{sweeps.length}</div>
              </div>
              <div className="table-block filler">
                <div className="table-block-head"></div>
                <div className="table-block-data"></div>
              </div>
            </div>
          </div>
          {sweeps ? 
            <table className="double">
              <thead>
                <tr>
                  <th>Sweep date</th>
                  <th>Sweep name</th>
                </tr>
              </thead>
              <tbody>
                {sweeps.map((sweep, index) => (
                  <tr key={sweep.sweepId}>
                    <td><Link title={sweep.name} to={`${user.userId}/sweeps/${sweep.sweepId}`}>{sweep.startDate}</Link></td>
                    <td><Link title={sweep.name} to={`${user.userId}/sweeps/${sweep.sweepId}`}>{sweep.name}</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          : <div class="wrapper">No sweeps to show.</div> }
        </Route>
      </Switch>
    );
  }
}

export default User;

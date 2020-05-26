import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function Snapshot() {
  let { userId, sweepId, snapshotId } = useParams();

  return (
    <div>
      <h3>Requested user ID: {userId}</h3>
      <h3>Requested sweep ID: {sweepId}</h3>
      <h3>Requested snapshot ID: {snapshotId}</h3>
    </div>
  );
}

export default Snapshot;

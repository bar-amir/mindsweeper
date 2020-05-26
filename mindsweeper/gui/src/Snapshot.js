import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
  const [snapshot, setSnapshot] = useState({});
  
  useEffect(async () => {
    const result = await axios(
      `http://localhost:5000/users/${userId}/snapshots/${snapshotId}`,
    );
 
    setSnapshot(result.data);
  }, []);

  return (
    <div>
      <h3>Requested user ID: {userId}</h3>
      <h3>Requested sweep ID: {sweepId}</h3>
      <h3>Requested snapshot ID: {snapshotId}</h3>
      {snapshot.results}
    </div>
  );
}

export default Snapshot;

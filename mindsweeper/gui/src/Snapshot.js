import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Head from './Head';
import Header from './Header';
import Loading from './Loading';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExpandArrowsAlt, faSyncAlt } from '@fortawesome/free-solid-svg-icons'
import {
  // BrowserRouter as Router,
  // Switch,
  // Route,
  Link,
  // useRouteMatch,
  useParams
} from "react-router-dom";
import './Snapshot.scss';
import { Breadcrumb, ProgressBar, Card, ListGroup, ListGroupItem, Button, OverlayTrigger, Popover } from 'react-bootstrap';

const API = `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}`

function normalizeFeelings(value){
  return ((value + 1) / 2) * 100
}

function Snapshot(props) {
  let { userId, snapshotId } = useParams();
  const [snapshot, setSnapshot] = useState({});
  const [pose, setPose] = useState({});
  const [feelings, setFeelings] = useState({});
  const [colorImage, setColorImage] = useState({});
  const [depthImage, setDepthImage] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const res_snapshot = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}`,
      );
      setSnapshot(res_snapshot.data);
  
      var res_colorImage = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/colorImage`,
      );
      res_colorImage.data.data = API + res_colorImage.data.data
      setColorImage(res_colorImage.data);
  
      var res_depthImage = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/depthImage`,
      );
      res_depthImage.data.data = API + res_depthImage.data.data
      setDepthImage(res_depthImage.data);
  
      var res_pose = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/pose`,
      );
      setPose(res_pose.data)
  
      var res_feelings = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/feelings`,
      );
      setFeelings(res_feelings.data)
      setIsLoading(false)
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (<div><Head /><Header /><Loading /></div>)
  }
  else {    
    var i;
    var nextId;
    var prevId;
    for (i = 0; i < props.snapshots.length; i++) {
      if (props.snapshots[i].snapshotId === snapshotId) {
        if (i > 0) {
          prevId = props.snapshots[i - 1].snapshotId
        }
        if (i < props.snapshots.length - 1) {
          nextId = props.snapshots[i + 1].snapshotId
        }
        break;
      }
    }
    
    const popOverTranslation = (
      <Popover id="popover-translation">
        <Popover.Title as="h3">Translation</Popover.Title>
        <Popover.Content>
          <strong>X:</strong> {pose.translation.x}<br />
          <strong>Y:</strong> {pose.translation.y}<br />
          <strong>Z:</strong> {pose.translation.z}<br />
        </Popover.Content>
      </Popover>
    )

    const popOverRotation = (
      <Popover id="popover-rotation">
        <Popover.Title as="h3">Rotation</Popover.Title>
        <Popover.Content>
          <strong>X:</strong> {pose.rotation.x}<br />
          <strong>Y:</strong> {pose.rotation.y}<br />
          <strong>Z:</strong> {pose.rotation.z}<br />
          <strong>W:</strong> {pose.rotation.w}<br />
        </Popover.Content>
      </Popover>
    )

    return (
      <div>
        <Head />
        <div className="snapshot color-image" style={{backgroundImage: `url(${colorImage.data})`}}>
          <Header variant="light" className="snapshot-header" />
          <Card className="snapshot-card m-3" style={{ width: '18rem' }}>
            <Card.Img title="Depth image" variant="top" src={depthImage.data} />
            <ListGroup className="list-group-flush">
              <ListGroupItem title="Date taken">{snapshot.datetime}</ListGroupItem>
              <ListGroupItem>
                <OverlayTrigger rootClose="true" trigger="click" placement="top" overlay={popOverTranslation}>
                  <Button title="Translation" className="mr-1">
                    <FontAwesomeIcon icon={faExpandArrowsAlt}/>
                  </Button>
                </OverlayTrigger>
                <OverlayTrigger rootClose="true" trigger="click" placement="top" overlay={popOverRotation}>
                  <Button title="Rotation">
                    <FontAwesomeIcon icon={faSyncAlt}/>
                  </Button>
                </OverlayTrigger>
              </ListGroupItem>
              <ListGroupItem>
                <ProgressBar title={feelings.hunger} className="mb-1" now={normalizeFeelings(feelings.hunger)} label="Hunger" />
                <ProgressBar title={feelings.thirst} className="mb-1" now={normalizeFeelings(feelings.thirst)} label="Thirst" />
                <ProgressBar title={feelings.exhaustion} className="mb-1" now={normalizeFeelings(feelings.exhaustion)} label="Exhaustion" />
                <ProgressBar title={feelings.happiness} now={normalizeFeelings(feelings.happiness)} label="Happiness" />
              </ListGroupItem>
            </ListGroup>
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                {prevId ? <Card.Link href="#"><Link title="Previous snapshot" to={`../snapshots/${prevId}`}>Previous</Link></Card.Link> : ''}
                {nextId ? <Card.Link href="#"><Link title="Next snapshot" to={`../snapshots/${nextId}`}>Next</Link></Card.Link> : ''}
                </div>
                <Card.Link href="#"><Link title="Return to sweep" to={`/users/${props.user.userId}/sweeps/${props.sweep.sweepId}`}>Return</Link></Card.Link>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>
    );
  }
}

export default Snapshot;

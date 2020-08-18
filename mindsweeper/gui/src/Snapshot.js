import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLongArrowAltLeft, faBroom, faLongArrowAltRight } from '@fortawesome/free-solid-svg-icons'
import {
  useParams
} from "react-router-dom";
import { HashLink as Link } from 'react-router-hash-link';

const API = `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}`

function normalizeFeelings(value){
  return ((value + 1) / 2) * 100
}

function Snapshot(props) {
  let { userId, snapshotId } = useParams();
  const [snapshot, setSnapshot] = useState({});
  // const [pose, setPose] = useState({});
  const [feelings, setFeelings] = useState({});
  const [colorImage, setColorImage] = useState({});
  const [depthImage, setDepthImage] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const res_snapshot = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}`,
      );
      setSnapshot(res_snapshot.data);
  
      var res_colorImage = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/colorImage`,
      )
      .then(function (response) {
        response.data.data = API + response.data.data
        setColorImage(response.data);
      })
      .catch(function (error) {
        console.log(error);
        setColorImage(null);
      });
  
      var res_depthImage = await axios.get(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/depthImage`,
      )
      .then(function (response) {
        response.data.data = API + response.data.data
        setDepthImage(response.data);
      })
      .catch(function (error) {
        console.log(error);
        setDepthImage(null);
      });
      
  
      // var res_pose = await axios(
      //   `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/pose`,
      // );
      // setPose(res_pose.data)
  
      var res_feelings = await axios(
        `http://${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}/users/${userId}/snapshots/${snapshotId}/feelings`, { timeout: 5000 }
      )
      .then(function (response) {
        setFeelings(response.data)
      })
      .catch(function (error) {
        console.log(error);
        setFeelings(null)
      });
      
      setIsLoading(false)
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (<div className="bg"></div>)
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

    var meters = '';
    if (feelings) {
      meters = <div className="meters">
                {feelings.hunger ?
                  <div className="meter-box">
                    <div className="meter" style={{width: normalizeFeelings(feelings.hunger) + '%'}}><span>Hunger</span></div>
                  </div>
                : ''}
                {feelings.thirst ?
                  <div className="meter-box">
                    <div className="meter" style={{width: normalizeFeelings(feelings.thirst) + '%'}}><span>Thirst</span></div>
                  </div>
                  : ''}
                {feelings.exhaustion ?
                  <div className="meter-box">
                    <div className="meter" style={{width: normalizeFeelings(feelings.exhaustion) + '%'}}><span>Exhaustion</span></div>
                  </div>
                  : ''}
                {feelings.happiness ?
                  <div className="meter-box">
                    <div className="meter" style={{width: normalizeFeelings(feelings.happiness) + '%'}}><span>Happiness</span></div>
                  </div>
                  : ''}
              </div>
    }

    return (
      <div className="bg">
        <div className="info">
          {depthImage ?
          <img alt="Depth map" src={depthImage.data} /> :
          ''}
          {meters}
          <div className="buttons">
            {prevId ? <Link to={`../snapshots/${prevId}`} className="button"><span><FontAwesomeIcon className="icon" icon={faLongArrowAltLeft}/><br />Prev</span></Link> : <a className="button deactivate"><span><FontAwesomeIcon className="icon" icon={faLongArrowAltLeft}/><br />Prev</span></a>}
            {nextId ? <Link to={`../snapshots/${nextId}`} className="button"><span><FontAwesomeIcon className="icon" icon={faLongArrowAltRight}/><br />Next</span></Link> : <a className="button deactivate"><span><FontAwesomeIcon className="icon" icon={faLongArrowAltRight}/><br />Next</span></a>}
            <Link to={`/users/${props.user.userId}/sweeps/${props.sweep.sweepId}#${snapshot.snapshotId}`} className="button back"><span><FontAwesomeIcon className="icon" icon={faBroom}/><br />Back to sweep</span></Link>
          </div>
        </div>
        {colorImage ?
          <div className="snapshot color-image" style={ {backgroundImage: `url(${colorImage.data})`}}></div>
        : ''}
      </div>
    );
  }
}

export default Snapshot;

import React from 'react';
import Brain from './Brain';
import { Link } from "react-router-dom";

function Header(props) {
  return (
    <div className="wrapper">
      <Brain />
      <div className="brand"><Link to="/">MindsweEpeR</Link></div>
    </div>
  );
}

export default Header;

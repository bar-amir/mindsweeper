import React from 'react';
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="wrapper">
      <p>Welcome to the graphical user interface of Mindsweeper™, where you can comfortably go through your test subjects' snapshots.</p>
      <ul className="links">
        <li><Link title="Explore test subjects" to="users">Explore test subjects</Link></li>
        <li><a title="Overview" href="https://bar-amir.github.io/mindsweeper" target="_blank" rel="noopener noreferrer">Overview</a></li>
        <li><a title="Repository" href="https://github.com/bar-amir/mindsweeper" target="_blank" rel="noopener noreferrer">Repository</a></li>
        <li><a title="Documentation" href="https://mindsweeper.readthedocs.io/" target="_blank" rel="noopener noreferrer">Documentation</a></li>
      </ul>
    </div>
  );
}

export default Home;

import React from 'react';
import Head from './Head';
import Header from './Header';
import { Breadcrumb, Button } from 'react-bootstrap';
import './Home.scss';

function Home() {
  return (
    <div>
      <Head />
      <Header variant="light" />
      <div className="home mt-5">
        <img src="/home.jpg" alt="Welcome" title="Welcome" />
        <h1>Welcome to Mindsweeper!</h1>
        <div>
          <Button variant="primary" size="lg" className="mr-1" title="Github" href="https://github.com/bar-amir/mindsweeper/" target="_blank">
            Github
          </Button>
          <Button variant="primary" size="lg" title="Documentation" href="https://mindsweeper.readthedocs.io/en/latest/?badge=latest" target="_blank">
            Documentation
          </Button>
        </div>
      </div>
    </div>
  );
}

export default Home;

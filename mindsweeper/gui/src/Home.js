import React from 'react';
import Head from './Head';
import Header from './Header';
import { Breadcrumb, Button } from 'react-bootstrap';
import './Home.scss';

function Home() {
  return (
    <div>
      <Head />
      <Header />
      <Breadcrumb className="m-3">
        <Breadcrumb.Item href="#" active>Home</Breadcrumb.Item>
      </Breadcrumb>
      <div className="home">
        <img src="/home.jpg" />
        <h1>Welcome to Mindsweeper!</h1>
        <div>
          <Button variant="primary" size="lg" className="mr-1" href="https://github.com/bar-amir/mindsweeper/" target="_blank">
            Github
          </Button>
          <Button variant="primary" size="lg" href="https://mindsweeper.readthedocs.io/en/latest/?badge=latest" target="_blank">
            Documentation
          </Button>
        </div>
      </div>
    </div>
  );
}

export default Home;

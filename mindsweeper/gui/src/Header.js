import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  NavLink,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";
import { Helmet } from "react-helmet";
import { Nav, Navbar, NavItem } from 'react-bootstrap';

function Header() {
  return (
    <Navbar bg="light" expand="lg">
      <Navbar.Brand>Mindsweeper</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link><NavLink exact activeClassName="nav-link-active" to="/">Home</NavLink></Nav.Link>
          <Nav.Link><NavLink activeClassName="nav-link-active" to="/users/">Users</NavLink></Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;

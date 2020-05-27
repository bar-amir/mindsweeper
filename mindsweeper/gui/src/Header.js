import React from 'react';
import {
  NavLink,
  Link
} from "react-router-dom";
import { Nav, Navbar } from 'react-bootstrap';

function Header(props) {
  return (
    <Navbar className={props.className} bg={props.variant} variant={props.variant} expand="lg">
      <Navbar.Brand><Link className="navbar-brand" title="Mindsweeper" to="/">Mindsweeper</Link></Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link><NavLink title="Home" exact className="nav-link" activeClassName="nav-link-active" to="/">Home</NavLink></Nav.Link>
          <Nav.Link><NavLink title="Users" className="nav-link" activeClassName="nav-link-active" to="/users/">Users</NavLink></Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;

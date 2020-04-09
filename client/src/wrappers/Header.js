import React from 'react';
import { Link } from 'react-router-dom';

export default function Header(props) {
  return (
    <header>
      <nav>
        <span><Link className="nav-elem" to='/'>Home</Link></span>
        <span><Link className="nav-elem" to='/posts'>Posts</Link></span>
        <span><Link className="nav-elem" to='/authors'>Authors</Link></span>
        {props.user ? <span onClick={props.logout}>Logout</span> : ''}
        {props.user ? <span><Link className="nav-elem" to='/posts/add'>Create a Post</Link></span> : ''}
      </nav>
    </header>
  )
}
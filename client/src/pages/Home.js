import React from 'react';
import { Redirect } from 'react-router-dom';

export default function Home(props) {
  if (!props.user) return <Redirect to='/auth' />

  return (
    <div>
      <h3>Welcome {props.user.name}!</h3>
    </div>
  )
}
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default function Home(props) {
  const [greeting, setGreeting] = useState('')

  useEffect(() => {
    if (props.user && props.token) {
      axios.get(`${process.env.REACT_APP_SERVER_URL}/api/protected`, {
        headers: {
          "Authorization": `Bearer ${props.user.token}`
        }
      }).then(response => {
        console.log(response.data)
        setGreeting(response.data.data)
      })
    }
  }, [props.user])

  if (!props.user) return <Redirect to='/auth' />

  return (
    <div>
      <h2>HOME</h2>
      <h3>{greeting}</h3>
      <p>Your email is {props.user.email}</p>
    </div>
  )
}
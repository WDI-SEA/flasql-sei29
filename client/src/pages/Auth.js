import React, { useState } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default function Auth(props) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [bio, setBio] = useState('');
  const [redirect, setRedirect] = useState(false);

  const handleLoginSubmit = e => {
    e.preventDefault()
    axios.post(`${process.env.REACT_APP_SERVER_URL}/auth/login`, { email, password })
    .then(response => {
      console.log(response.data)
      if (response.data.mesage) {
        props.setUserToken(null)
      } else {
        props.setUserToken({ user: response.data.user, token: response.data.token})
        setRedirect(true)
      }
    }).catch(err=>console.log(err))
  }
  
  const handleSignupSubmit = e => {
    e.preventDefault()
    let payload = {email, password, name}
    if (bio) payload.bio = bio
    console.log(payload)

    axios.post(`${process.env.REACT_APP_SERVER_URL}/users`, payload)
    .then(response => {
      console.log('🏴‍☠️')
      console.log(response.data)
      if (response.data.mesage) {
        props.setUserToken(null)
      } else {
        props.setUserToken({ user: response.data.user, token: response.data.token})
        setRedirect(true)
      }
    }).catch(err=>console.log(err))
  }
  
  if (redirect || props.user) return <Redirect to='/' />

  return (
    <div className="auth-container">
      <div className="auth-panel">
        <h3>Login</h3>
        <form onSubmit={handleLoginSubmit}>
          <div>
            <label>Email: </label>
            <input type="email" onChange={e=>setEmail(e.target.value)} />
          </div>
          <div>
            <label>Password: </label>
            <input type="password" onChange={e=>setPassword(e.target.value)} />
          </div>
          <div>
            <input type="submit" value="Login" />
          </div>
        </form>
      </div>
      <div className="divider"></div>
      <div className="auth-panel">
        <h3>Signup</h3>
        <form onSubmit={handleSignupSubmit}>
          <div>
            <label>Name: </label>
            <input required type="text" onChange={e=>setName(e.target.value)} />
          </div>
          <div>
            <label>Email: </label>
            <input required type="email" onChange={e=>setEmail(e.target.value)} />
          </div>
          <div>
            <label>Bio: </label>
            <input type="text" onChange={e=>setBio(e.target.value)} />
          </div>
          <div>
            <label>Password: </label>
            <input required type="password" onChange={e=>setPassword(e.target.value)} />
          </div>
          <div>
            <input type="submit" value="Signup" />
          </div>
        </form>
      </div>
    </div>
  )
}
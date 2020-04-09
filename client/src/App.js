import React, { useState } from 'react';
import './App.css';
import {BrowserRouter as Router} from 'react-router-dom';
import Header from './wrappers/Header';
import Content from './pages/Content';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const setUserToken = (responseData) => {
    if (responseData) {
      console.log("🐻")
      setToken(responseData.token)
      setUser(responseData.user)
    } else {
      setToken(null)
      setUser(null)
    }
  }
  const updateUser = newUserDeets => {
    setUser(newUserDeets)
  }

  return (
    <Router>
      <div className="App">
        <Header logout={() => setUserToken(null)} user={user} />
        <main>
          <Content user={user} token={token} setUserToken={setUserToken} updateUser={updateUser} />
        </main>
      </div>
    </Router>
  );
}

export default App;

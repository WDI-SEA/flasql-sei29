import React, { useState } from 'react';
import './App.css';
import {BrowserRouter as Router} from 'react-router-dom';
import Header from './wrappers/Header';
import Content from './pages/Content';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const setUserToken = (imputedUser, imputedToken) => {
    setUser(imputedUser)
    setToken(imputedToken)
  }

  return (
    <Router>
      <div className="App">
        <Header logout={() => setUserToken(null, null)} user={user} />
        <main>
          <Content user={user} setUser={setUser} setToken={setToken} token={token} />
        </main>
      </div>
    </Router>
  );
}

export default App;

import React from 'react';
import {Route, Switch} from 'react-router-dom';
import Home from './Home';
import Auth from './Auth';
import NewPost from './NewPost';
import ShowPost from './ShowPost';
import Posts from './Posts';
import Authors from './Authors';

export default function Content(props) {
  return (
    <div className="App-content">
      <Switch>
        <Route exact path="/" render={() => <Home user={props.user} token={props.token} />} /> />
        <Route path='/auth' render={() => <Auth user={props.user} setUserToken={props.setUserToken} />} /> />
        <Route path="/posts/add" render={() => <NewPost user={props.user} />} />
        <Route path="/posts/:id" render={() => <ShowPost user={props.user} />} />
        <Route path="/posts" component={Posts} />
        <Route path="/authors" component={Authors} />
      </Switch>
    </div>
  )
}
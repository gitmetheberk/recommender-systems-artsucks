import './App.css';
import React, { Component } from 'react';

// Import components
import ImageWindow from './components/imageWindow';
import HistorySidebar from './components/historySidebar'
import Login from './components/login'

// Other items lower on the priorities list
//import RoboticStatusBar from './components/roboticStatusBar'
// Make history panel and login sidebar collapsable

class App extends Component {
  state = {
    token: ""
  }

  receiveToken(rectoken) {
    this.setState({token: rectoken})
  }

  render(){
    return (
      <div className="d-flex flex-row justify-content-between ">
        <div className="p-0"><HistorySidebar /></div>
        <div className="p-5"><ImageWindow token={this.state.token}/></div>
        <div className="p-0"><Login sendToken={this.receiveToken.bind(this)}/></div>
      </div>
    );
  }
}

export default App;

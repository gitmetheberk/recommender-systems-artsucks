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
    token: "",
    updateHistory: false
  }

  receiveToken(rectoken) {
    this.setState({token: rectoken})
  }

  // Uses a lazy toggle to trigger historySidebar props changes
  updateHistory(){
    this.setState({updateHistory: !this.state.updateHistory})
  }

  // TODO: Implement github links in bottom right
  render(){
    return (
      <div className="d-flex flex-row justify-content-between bg-light">
        <div className="p-0"><HistorySidebar token={this.state.token} updateHistory={this.state.updateHistory}/></div>
        <div className="p-5"><ImageWindow updateHistory={this.updateHistory.bind(this)} token={this.state.token}/></div>
        <div className="p-0"><Login sendToken={this.receiveToken.bind(this)}/></div>
      </div>
    );
  }
}

export default App;

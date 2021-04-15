import './App.css';
import React, { Component } from 'react';

// Import components
import ImageWindow from './components/imageWindow';
import HistorySidebar from './components/historySidebar'
import Login from './components/login'
import InfoBox from './components/infoBox'

// Other items lower on the priorities list
// import RoboticStatusBar from './components/roboticStatusBar'
// Make history panel and login sidebar collapsable

// Request URL, use 104... for a server commit, use local for testing
const requestUrl = "http://104.236.113.146:8010/proxy/"
// const requestUrl = "http://localhost:8010/proxy/"

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

  render(){
    return (
      <div className="d-flex flex-row justify-content-between bg-light">
        <div className="p-0"><HistorySidebar token={this.state.token} updateHistory={this.state.updateHistory} requestUrl={requestUrl}/></div>
        <div className="p-2"><ImageWindow updateHistory={this.updateHistory.bind(this)} token={this.state.token} requestUrl={requestUrl}/></div>
        <div className="d-flex flex-column align-items-end">
          <div className="p-0"><Login sendToken={this.receiveToken.bind(this)} requestUrl={requestUrl}/></div>
          <div className="p-0 mt-auto"><InfoBox requestUrl={requestUrl}/></div>
        </div>
      </div>
    );
  }
}

export default App;

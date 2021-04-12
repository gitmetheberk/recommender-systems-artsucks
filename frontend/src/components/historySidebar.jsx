import React, { Component } from 'react';
import axios from 'axios'
import HistoryLine from './historyLine'

// FIXME: Find a better way than hardcoding this in multiple files
// Using local-cors-proxy node js module
const requestUrl = "http://localhost:8010/proxy/"

class HistorySidebar extends Component {
    state = { 
        history: {},
     }

    // On component update, only if props changes, run getHistory
    componentDidUpdate(prevProps, prevState){
        if (prevProps !== this.props){
            this.getHistory();
        }
    }

    getHistory(){
        if (this.props.token !== ""){
            let token = this.props.token
            axios.get(requestUrl + 'api/getrecenthistory', {
                headers :{
                'Authorization': `token ${token}`
            }})
            .then((res) => this.setState({history: res.data}))
            .catch((err) => {
                console.log(`Error retrieving history: ${err}`)
            })
        }
    }

    renderHistoryLines(){
        // Convert the JSON object to a simple list for map
        let history = Object.values(this.state.history)

        return history.map((line) => {
            return (
            <li class="list-group-item bg-primary">
                <HistoryLine history={line}/>
            </li>
    
        )
    });
    }

    render() { 
        return ( 
            <div style={{width: '250px', height: '800px'}} className="rectangle bg-info rounded-right">
                <div className="card border-0">
                    <div class="card-header bg-info">
                        <h4><p className="text-center">Your History</p></h4>
                    </div>
                    <ul class="list-group list-group-flush">
                        {this.renderHistoryLines()}
                    </ul>
                </div>
            </div>
         );
    }
}
 
export default HistorySidebar;
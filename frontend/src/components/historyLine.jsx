import React, { Component } from 'react';

class HistoryLine extends Component {
    state = {  }
    render() { 
        let date = new Date(Date.parse(this.props.history.updated))
        return ( 
            <div className="">
                <span className="text-right">{this.props.history.status === "L" ? '✅' : '❌'}</span>
                <span className="font-weight-bold">{this.props.history.artist}</span>
                <br/>
                <span>{date.toLocaleString()}</span>
            </div> 
        );
    }
}
 
export default HistoryLine;
import React, { Component } from 'react';

class InfoBox extends Component {
    state = { 
        
     }

    render() { 
        return ( 
            <div style={{width: '105px', height: '100px'}} className="d-flex flex-column justify-content-center align-items-center rectangle bg-info rounded-left">
                    <a style={{color: "#5cc41f"}} className="h4 p-0" href="https://github.tamu.edu/jared-pauletti/art-recommender">Github</a>
                    <a style={{color: "#50d9ae"}} className="h4 p-0" href="datasets.html">Datasets</a>
            </div>
        );
    }
}
 
export default InfoBox;

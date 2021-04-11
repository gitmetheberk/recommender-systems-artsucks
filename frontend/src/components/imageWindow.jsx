import React, { Component } from 'react';
import axios from 'axios'

// FIXME: Find a better way than hardcoding this in multiple files
// Using local-cors-proxy node js module run
const requestUrl = "http://localhost:8010/proxy/"

class ImageWindow extends Component {

    state = { 
        imageTitle: "",
        imageUrl: "",
        imageId: -1,
     }

    getNewImage(){
        // Send a get request to get the url of the next image
        let token = this.props.token
        axios.get(requestUrl + 'api/getnewart', {
            headers :{
            'Authorization': `token ${token}`
        }})
        .then((res) => this.updateImage(res))
        .catch((err) => {
            console.log(err)
        })
    }
    
    // Updates state after receiving new data
    updateImage(res){
        let imageUrl = requestUrl + "static/images/" + res.data.filename;
        this.setState({
            imageUrl: imageUrl,
            imageArtist: res.data.artist,
            imageId: res.data.id
        })
    }

    // Runs when either like or dislike is clicked, liked=true if liked, else dislike
    handleClick(liked){
        // Send a put request updating the user's rating for the image
        // Note: Using put instead of post in the event we end up doubling over some images
        //let imageId = this.imageId;
        let imageId = 3;
        let token = this.props.token;
        // TODO Programatically don't require the user for post requests in the backend, let it be chosen by the token
        axios.post(requestUrl + 'api/historylines/', {artwork: imageId, status: liked ? 'L' : 'D', user:4},
        {
            headers :{
            'Authorization': `token ${token}` 
        }})
        .catch((err) => {
            console.log(err)
        });

        this.getNewImage();
    }

    checkLoggedIn(){
        if (this.props.token !== ""){
            this.getNewImage()
        } else {
            alert("Something tells me you don't really want to appreciate art...")
        }
    }

    render() { 
        if (this.state.imageId === -1){
            return (
                <div>
                    <h3>Howdy! Please log in to receive your full art appreciation experience</h3>
                    <button onClick={() => this.checkLoggedIn()} className="btn btn-danger btn-block btn-lg">I have logged in and I am ready to appreciate art</button>
                </div>
            )
        } else {
            return (
                <div style={{width: 1000, height: 650}} className="d-flex flex-column">
                    <div style={{width: 1000, height: 650}} className="rounded bg-secondary d-flex justify-content-center align-items-center">
                        <img style={{display: "block", 'max-width': 1000, 'max-height': 600, width: 'auto', height: 'auto'}}
                            src={this.state.imageUrl} 
                            alt={this.state.imageTitle}>
                        </img>
                    </div>
    
                    <div className="pt-1">
                        <button onClick={() => this.handleClick(false)} className="btn btn-warning w-50">Dislike</button>
                        <button onClick={() => this.handleClick(true)} className="btn btn-success w-50">Like</button>
                    </div>
                </div>
            );
        }
    }
}
 
export default ImageWindow;
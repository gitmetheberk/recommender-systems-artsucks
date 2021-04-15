import React, { Component } from 'react';
import axios from 'axios'


class ImageWindow extends Component {

    state = { 
        imageTitle: "",
        imageUrl: "",
        imageId: -1,
     }

    getNewImage(){
        // Send a get request to get the url of the next image
        let token = this.props.token
        axios.get(this.props.requestUrl + 'api/getnewart', {
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
        let imageUrl = this.props.requestUrl + "static/images/" + res.data.filename;
        this.setState({
            imageUrl: imageUrl,
            imageArtist: res.data.artist,
            imageId: res.data.id
        })
    }

    // TODO: When a user likes or dislikes an image, disable the buttons until the .then in getNewImage()
    // Runs when either like or dislike is clicked, liked=true if liked, else dislike
    handleClick(liked){
        // Send a post request updating the user's rating for the image
        let image = this.state.imageId;
        let token = this.props.token;
        axios.post(this.props.requestUrl + 'api/historylines/', {artwork: image, status: liked ? 'L' : 'D'},
        {
            headers :{
            'Authorization': `token ${token}` 
        }})
        .then(() => {
            // After response received, update history
            this.props.updateHistory()
        })
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
            // Technically I put this in originally because I didn't know how to signal between components
            // However, I like it better than having it start automatically, just for the sake of the joke
            // So it's staying in
            return (
                <div>
                    <h3>Howdy! Please log in to receive your full art appreciation experience</h3>
                    <button onClick={() => this.checkLoggedIn()} className="btn btn-danger btn-block btn-lg">I have logged in and I am ready to appreciate art</button>
                </div>
            )
        } else {
	    let dims = {width: 1200, height: 780};
            return (
                <div style={dims} className="d-flex flex-column">
                    <div style={dims} className="rounded bg-secondary d-flex justify-content-center align-items-center">
                        <img style={{display: "block", 'maxWidth': dims.width, 'maxHeight': dims.height-50, width: 'auto', height: 'auto'}}
                            src={this.state.imageUrl} 
                            alt={this.state.imageTitle}>
                        </img>
                    </div>
    
                    <div className="pt-1">
                        <button onClick={() => this.handleClick(false)} className="btn btn-warning w-50 font-weight-bold">Dislike</button>
                        <button onClick={() => this.handleClick(true)} className="btn btn-success w-50 font-weight-bold">Like</button>
                    </div>
                </div>
            );
        }
    }
}
 
export default ImageWindow;

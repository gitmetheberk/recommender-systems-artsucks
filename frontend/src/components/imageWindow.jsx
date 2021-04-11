import React, { Component } from 'react';
import axios from 'axios'

// FIXME: Find a better way than hardcoding this in multiple files
// Using local-cors-proxy node js module run
const requestUrl = "http://localhost:8010/proxy/"

class ImageWindow extends Component {

    state = { 
        imageTitle: "",
        imageUrl: requestUrl + "static/images/loading.gif",  // Default to a loading gif
        //imageUrl: "http://localhost:8000/static/images/Eugene_Delacroix_7.jpg",
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

    // TODO If we don't have a token, show a "please sign in message" or pull for random artworks
    // TODO Find a way to make the image box consistent, ex. images all scale to the same maximum width AND HEIGHT
    render() { 
        return (
            <div className="h-auto">
                <img className="rounded mw-100 mh-auto"
                    src={this.state.imageUrl} 
                    alt={this.state.imageTitle}>
                </img>

                <div>
                    <button onClick={() => this.handleClick(false)} className="btn btn-secondary w-50">Dislike</button>
                    <button onClick={() => this.handleClick(true)} className="btn btn-success w-50">Like</button>
                </div>
            </div>
        );
    }
}
 
export default ImageWindow;
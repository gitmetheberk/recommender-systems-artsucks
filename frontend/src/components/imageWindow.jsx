import React, { Component } from 'react';
import axios from 'axios'

// Using local-cors-proxy node js module run
const requestUrl = "http://localhost:8010/proxy/"

class ImageWindow extends Component {
    state = { 
        imageTitle: "",
        imageUrl: requestUrl + "static/images/loading.gif",  // Default to a loading gif
        //imageUrl: "http://localhost:8000/static/images/Eugene_Delacroix_7.jpg",
        imageId: -1,
     }


    // On first load, get a new image
    componentDidMount() {
        this.getNewImage();
    }
    
    // Updates state after receiving new data
    updateImage(res){
        let imageUrl = requestUrl + "static/images/" + res.filename;
        this.setState({
            imageUrl: imageUrl,
            imageArtist: res.artist,
            imageId: res.id
        })
    }

    getNewImage(){
        // Send a get request to get the url of the next image
        axios.get(requestUrl + 'api/artworks')
        .then((res) => this.updateImage(res))
    }

    // Runs when either like or dislike is clicked, liked=true if liked, else dislike
    handleClick(liked){
        // Send a put request updating the user's rating for the image
        // Note: Using put instead of post in the event we end up doubling over some images
        axios.put(requestUrl + 'api/historylines', {imageId: this.imageId, like: liked});

        this.getNewImage();
    }


    // TODO Find a way to make the image box consistent, ex. images all scale to the same maximum width AND HEIGHT
    render() { 
        return (
            <div className="h-auto">
                <img className="rounded mw-100 mh-auto"
                    src={this.state.imageUrl} 
                    alt={this.state.imageTitle}>
                </img>

                <div>
                    <button onClick={() => this.handleClick(true)} className="btn btn-secondary w-50">Dislike</button>
                    <button onClick={() => this.handleClick(false)} className="btn btn-success w-50">Like</button>
                </div>
            </div>
        );
    }
}
 
export default ImageWindow;
import React, { Component } from 'react';
import axios from 'axios'

// FIXME: Find a better way than hardcoding this in multiple files
// Using local-cors-proxy node js module run
const requestUrl = "http://localhost:8010/proxy/"

class Login extends Component {
    state = { 
        logged_in: false,
        username: "",
        password: "",
        token: ""
     }

    login(event){
        // Stops the website from reloading on submit
        event.preventDefault()

        // This probably has something to do with the async nature of things, but I can't directly
        // reference this.state in the post request, so these have to be here, otherwise the entire
        // payload is blank (which causes a lot of headaches...)
        let username = this.state.username;
        let password = this.state.password;

        // Send an auth request to the server
        axios.post(requestUrl + 'api-token-auth/', {
                username: username,
                password: password
        })
        .then((res) => {
            this.setState({
                token: res.data.token,
                logged_in: true
            });

            // Clear the user's password
            this.setState({password: ""})

            // Pass the token up to the parent object App
            this.props.sendToken(this.state.token);
        })
        .catch((error) => {
            this.setState({password: ""})
            console.log(error)
        })
    }

    // Active event handlers for state changes in the input fields
    updateUsername(evt){
        this.setState({username: evt.target.value})
    }

    updatePassword(evt){
        this.setState({password: evt.target.value})
    }

    render() { 
        if (this.state.logged_in === true){
            return (
                <div className="d-flex p-2 bg-secondary flex-column rounded-left">
                <div>
                    <h5 >Welcome,</h5>
                    <h5 className="float-right">{this.state.username}!</h5>
                </div>
                </div>
            )
        }  // Else
        return ( 
            <div className="d-flex p-2 bg-secondary flex-column rounded-left">
                <h5 className="">Login</h5>
                <form onSubmit ={(event) => this.login(event)}>
                    <div className="p-1">
                    <input value={this.state.username} onChange={evt => this.updateUsername(evt)} placeholder="Username" type="text" name="username" />
                    </div>
                    <div className="p-1">
                    <input value={this.state.password} onChange={evt => this.updatePassword(evt)} placeholder="Password" type="password" name="password" />
                    </div>
                    <div className="p-1">
                        <input type="submit" value="Login" className="float-right"/>
                    </div>
                </form>
            </div>
         );
    }
}
 
export default Login;
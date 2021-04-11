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

    formSubmit(event){
        // Stops the website from reloading on submit
        event.preventDefault()
        this.login()
    }

    login(){
        let username = this.state.username;
        let password = this.state.password;

        // Send an auth request to the server
        axios.post(requestUrl + 'auth/api-token-auth/', {
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
            alert("There was an error loggin you in. Please try again.")
            console.log(error)
        })
    }

    register(){
        let username = this.state.username;
        let password = this.state.password;

        // Register the new user
        axios.post(requestUrl + 'auth/register/', {
            username: username,
            password: password
        })
        .then((res) => {
            this.login()
        })
        .catch((error) => {
            this.setState({password: "", username: ""})
            alert("There was an error creating your account. Please try again.")
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
                <h5 className="">Login or Register</h5>
                <form onSubmit ={(event) => this.formSubmit(event)}>
                    <div className="p-1">
                    <input value={this.state.username} onChange={evt => this.updateUsername(evt)} placeholder="Username" type="text" name="username" />
                    </div>
                    <div className="p-1">
                    <input value={this.state.password} onChange={evt => this.updatePassword(evt)} placeholder="Password" type="password" name="password" />
                    </div>
                    </form>
                <div className="p-1 btn-group btn-group-justified">
                    <button onClick={() => this.login()} className="float-left btn btn-success w-50">Login</button>
                    <button onClick={() => this.register()} className="float-right btn btn-primary w-50">Register</button>
                </div>
            </div>
         );
    }
}
 
export default Login;
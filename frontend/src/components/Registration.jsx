import React, { useState, useContext, useEffect } from 'react';
import { Card, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import LoginContext from "../contexts/loginContext";

// import github logo from fontawesome
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

import axios from 'axios';

import "./Registration.css";

function Registration() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState('');

  const [wantToRegister, setWantToRegister] = useState(false);
  const [buttonText, setButtonText] = useState("Login");
  const [switchText, setSwitchText] = useState("Don't have an account? Register here.");

  const [loggedIn, setLoggedIn] = useContext(LoginContext);

  useEffect(() => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const code = urlParams.get("code");
    if (code) {
        axios.get(`http://localhost:5000/github_login?code=${code}`)
            .then(response => {
                setLoggedIn(response.data.username); // login the user
                navigate('/'); // redirect to home page

            })
            .catch(error => {
                // handle the error
            });
    }
}, []);

  const navigate = useNavigate();

  const handleUsername = (event) => {
    setUsername(event.target.value);
  }

  const handlePassword = (event) => {
    setPassword(event.target.value);
  }

  const handleEmail = (event) => {
    setEmail(event.target.value);
  }

  const handleSwitch = () => {
    wantToRegister ? setWantToRegister(false) : setWantToRegister(true);
    if (wantToRegister) {
      setButtonText("Login");
      setSwitchText("Don't have an account? Register here.")
    } else {
      setButtonText("Register");
      setSwitchText("Already have an account? Login here.");
    }
  }

  const handleLogin = () => {
    fetch('/login', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      }),
      credentials: 'include'
    }).then(res => {
      if (res.status === 200) {
        setLoggedIn(username);
      } else if (res.status === 401) {
        alert("username or password wrong");
      } else {
        throw new Error();
      }
    }).catch(err => console.log('login: ' + err));

    navigate('/');
  }

  const handleGitHubOAuth = async () => {
    window.location.assign(`https://github.com/login/oauth/authorize?client_id=${process.env.REACT_APP_GITHUB_CLIENT_ID}`);
  }

  const submit = () => {
    wantToRegister ? handleRegister() : handleLogin();
  }

  const handleRegister = () => {
    fetch('/register', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password,
        email: email
      }),
      credentials: 'include'
    }).then(res => {
      if (res.status === 201) {
        handleLogin();
      } else if (res.status === 409) {
        alert("username already taken");
      } else {
        throw new Error();
      }
    }).catch(err => console.log('register:' + err));
  }

  return (
    <div className='div-registration'>
      <Card className='card-custom'>
        <Card.Header className='card-header-custom'>
          <h5><b>Login</b> or <b>register an account</b> below!</h5>
        </Card.Header>
        <Card.Body>
          <Form>
            <Button
              onClick={handleGitHubOAuth}
              style={{
                backgroundColor: "#f5f5f5",
                color: "#333",
                borderRadius: "5px",
                padding: "10px 20px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                border: "1px solid #333",
                width: "100%",
                maxWidth: "400px",
                margin: "0 auto",
                fontSize: "16px",
                fontWeight: "bold"
              }}
            >
              Login with GitHub <FontAwesomeIcon icon={faGithub} style={{ marginLeft: "10px" }} />
            </Button>


            <Form.Group className='form-group-custom'>
              <Form.Label>Username</Form.Label>
              <Form.Control placeholder="Enter Username" onChange={handleUsername} />
            </Form.Group>
            <Form.Group className='form-group-custom'>
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Enter Password" onChange={handlePassword} />
            </Form.Group>
            {
              wantToRegister && (
                <Form.Group className='form-group-custom'>
                  <Form.Label>Email</Form.Label>
                  <Form.Control placeholder="Enter Email" onChange={handleEmail} />
                </Form.Group>
              )
            }
            <Button className='submit' variant="primary" type="submit" onClick={submit}>
              {buttonText}
            </Button>
            <Button className='submit' onClick={handleSwitch}>{switchText}</Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Registration;


import React, { useCallback, useState, useContext, useEffect } from 'react';
import { Card, Container, Form, Button, Row } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

import { FaGithub } from 'react-icons/fa'

import LoginContext from "../contexts/loginContext";

function Registration() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const [wantToRegister, setWantToRegister] = useState(false);

  const [loggedIn, setLoggedIn, savedProjects, setSavedProjects] = useContext(LoginContext);

  const navigate = useNavigate();

  const login = useCallback((id) => {
    fetch('/saved-projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "username": id })
    }).then(res => res.json()).then(json => {
      setSavedProjects(Object.values(json['projects']));
    })
    setLoggedIn(id);
  }, [setSavedProjects, setLoggedIn]);

  useEffect(() => {
    loggedIn !== '' && navigate('/');
  }, [loggedIn, navigate]);

  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    if (urlSearchParams.has('code')) {
      const code = urlSearchParams.get('code');
      fetch(`/github_login?code=${code}`).then(res => res.json()).then(json => {
        login(json.username);
      });
    }
  }, [login, navigate]);

  const handleUsername = (event) => {
    setUsername(event.target.value);
  }

  const handlePassword = (event) => {
    setPassword(event.target.value);
  }

  const handleEmail = (event) => {
    setEmail(event.target.value);
  }

  const handleGitHubOAuth = () => {
    const clientId = process.env.REACT_APP_GITHUB_CLIENT_ID;
    const url = `https://github.com/login/oauth/authorize?client_id=${clientId}`;

    window.location.assign(url);
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
        login(username);
      } else if (res.status === 401) {
        alert("username or password wrong");
      } else {
        throw new Error();
      }
    }).catch(err => alert('login: ' + err));

    // TODO: this navigate should not be necessary but is
    navigate('/')
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

  const submit = () => {
    wantToRegister ? handleRegister() : handleLogin();
  }

  const handleSwitch = () => {
    wantToRegister ? setWantToRegister(false) : setWantToRegister(true);
  }

  return (
    <>
      <Container className="mt-3">
        <Card style={{
          maxWidth: '450px',
          margin: '0 auto',
          marginTop: '20px',
          paddingBottom: '10px'
        }}>

          <Card.Header style={{
            width: '100%',
            fontSize: 'medium',
            textAlign: 'center'
          }}>
            <h5><b>Login</b> or <b>register an account</b> below!</h5>
          </Card.Header>

          <Card.Body>
            <Form>
    
                { /* Github Login */ }
                <Row>
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
                    Login with GitHub <FaGithub style={{ marginLeft: "10px" }} />
                  </Button>
                </Row>

                { /* Normal Login */ }
                <Row>
                  <Form.Group style={{padding: '10px'}}>
                    <Form.Label>Username</Form.Label>
                    <Form.Control placeholder="Enter Username" onChange={handleUsername} />
                  </Form.Group>
                  <Form.Group style={{padding: '10px'}}>
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter Password" onChange={handlePassword} />
                  </Form.Group>
                  {
                    wantToRegister && (
                      <Form.Group style={{padding: '10px'}}>
                        <Form.Label>Email</Form.Label>
                        <Form.Control placeholder="Enter Email" onChange={handleEmail} />
                      </Form.Group>
                    )
                  }
                </Row>

              { /* Login / Register / Switch */ }
              <Button style={{
                marginTop: '20px',
                width: '100%',
                padding: '10px 20px'
              }} variant="primary" type="submit" onClick={submit}>
                {wantToRegister ? 'Register' : 'Login'}
              </Button>
              <Button style={{
                marginTop: '20px',
                width: '100%',
                padding: '10px 20px'
              }} onClick={handleSwitch}>
                {wantToRegister ? 'Already have an account? Login here.' : "Don't have an account? Register here."}
              </Button>
              
            </Form>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
}

export default Registration;

import { useState, useContext } from 'react';
import { Card, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import LoginContext from "../contexts/loginContext";

// import github logo from fontawesome
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

import "./Registration.css";

const handleGitHubOAuth = () => {
  // Request the redirect URL from the server
  fetch('/github_oauth_url')
    .then(response => response.json())
    .then(data => {
      const { url } = data;
      // Redirect to the GitHub OAuth page
      window.location.href = url;
      // Make a request to the GitHub OAuth endpoint
      fetch('/github_oauth')
      //make sure response is 200
        .then(response => response.json())
        .then(data => {
          console.log(data);

    })
    .catch(err => console.log(err));
  })
  .catch(err => console.log(err));
}

function Registration() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState('');

  const [wantToRegister, setWantToRegister] = useState(false);
  const [buttonText, setButtonText] = useState("Login");
  const [switchText, setSwitchText] = useState("Don't have an account? Register here.");

  const [loggedIn, setLoggedIn] = useContext(LoginContext);

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

  return (
    <div className='div-registration'>

      <Card className='card-custom'>
        <Card.Header className='card-header-custom'>
          <h5><b>Login</b> or <b>register an account</b> below!</h5>
        </Card.Header>

        <Card.Body>
          <Form>
            <Button className='submit' variant="dark" type="button" onClick={handleGitHubOAuth}>
              Login with GitHub <FontAwesomeIcon icon={faGithub} />
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

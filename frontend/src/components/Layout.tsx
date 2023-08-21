import { useState } from 'react';
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link, Outlet, useNavigate } from 'react-router-dom';

import LoginContext from "../contexts/loginContext";

const Layout = () => {
    const [loggedIn, setLoggedIn] = useState('');
    const [savedProjects, setSavedProjects] = useState([]);

    const navigate = useNavigate();
    
    const handleLogout = () => {
        setLoggedIn('');
        setSavedProjects([]);
        fetch('/logout', {
            method: 'POST',
            credentials: 'include'
        }).catch(err => console.log('logout: ' + err));
        navigate('/registration');
    }

    return (
        <>
            <LoginContext.Provider value={[loggedIn, setLoggedIn, savedProjects, setSavedProjects]}>
                <Container fluid>
                    { /* Header */ }
                    <Navbar bg="light" variant="light">
                        <Container>
                                <Navbar.Brand as={Link} to='/'>pigeonhole.dev</Navbar.Brand>
                                {loggedIn !== '' && <Nav><Nav.Link as={Link} to='profile'>Profile</Nav.Link></Nav>}
                                <Nav className='ms-auto'>
                                    {loggedIn === '' && <Nav.Link as={Link} to="registration">Login / Register</Nav.Link>}
                                    {loggedIn !== '' && <Nav.Link onClick={handleLogout}>Logout</Nav.Link>}
                                </Nav>
                        </Container>
                    </Navbar>

                    { /* Content */ }
                    <Outlet />
                </Container>
            </LoginContext.Provider>
        </>
    );
};

export default Layout;
import { Link, Outlet } from 'react-router-dom';
import { Container, Navbar, Nav } from "react-bootstrap";

import { useState } from 'react';
import LoginContext from "../contexts/loginContext";

const Layout = () => {
    const [loggedIn, setLoggedIn] = useState('');

    const handleLogout = () => {
        setLoggedIn('');
        fetch('/logout', {
            method: 'POST',
            credentials: 'include'
        }).catch(err => console.log('logout: ' + err));
    }

    return (
        <>
            <LoginContext.Provider value={[loggedIn, setLoggedIn]}>
                <Container fluid>
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
                    <Outlet />
                </Container>
            </LoginContext.Provider>
        </>
    );
};

export default Layout;
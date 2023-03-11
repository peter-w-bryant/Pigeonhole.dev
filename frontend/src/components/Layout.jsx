import { Link, Outlet } from 'react-router-dom';
import { Container, Navbar, Nav} from "react-bootstrap";

const Layout = () => {
    return (
        <>
            <Container fluid>
                <Navbar bg="light" variant="light">
                    <Container>
                        <Navbar.Brand as={Link} to='/'>pigeonhole.dev</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav" />
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="ms-auto">
                                <Nav.Link as={Link} to='/projects'>Projects</Nav.Link>
                                <Nav.Link as={Link} to='/about'>About</Nav.Link>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
                <Outlet />
            </Container>
        </>
    );
};

export default Layout;
import json from '../assets/sample_data/all-projects.json';
import Project from './Project';
import { useEffect, useState } from 'react';
import { Container, Form, Navbar, Nav, FormControl, Button, Row, Col } from "react-bootstrap";

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [projects, setProjects] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredProjects, setFilteredProjects] = useState([]);

    useEffect(() => {
        setProjectData(json);
        const newProjects = Object.values(projectData).map(value => value);
        setProjects(newProjects);
        setFilteredProjects(newProjects);
    }, [projectData]);

    const handleSearch = (event) => {
        const searchTerm = event.target.value.toLowerCase(); 
        const newFilteredProjects = searchTerm ? filteredProjects.filter(project => {
            const gh_repo_name = project.gh_repo_name?.toLowerCase();
            return gh_repo_name.includes(searchTerm);
        }) : projects;
        setFilteredProjects(newFilteredProjects);
        setSearchTerm(searchTerm);
    };


    return (
        <Container fluid>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand href="#home">pigeonhole.dev</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link href="#projects">Projects</Nav.Link>
                        <Nav.Link href="#about">About</Nav.Link>
                    </Nav>
                    <Form inline>
                        <FormControl type="text" placeholder="Search projects" className="mr-sm-2" value={searchTerm} onChange={handleSearch} />
                        <Button variant="outline-primary">Search</Button>
                    </Form>
                </Navbar.Collapse>
            </Navbar>
            <Row className="g-4">
                {
                    filteredProjects.map(project => {
                        return (
                            <Col style={{ display: 'flex' }} xs={12} sm={6} md={4} key={`${project.pUID}-${project.title}`}>
                                <Project {...project} />
                            </Col>
                        );
                    })
                }
            </Row>
        </Container>
    );
};

export default Home;

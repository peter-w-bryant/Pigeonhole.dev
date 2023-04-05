import React, { useContext, useEffect, useState } from 'react';
import { Col, Container, Row } from "react-bootstrap";

import Project from './Project';
import SearchBox from './SearchBox';

import LoginContext from "../contexts/loginContext";

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [filteredProjects, setFilteredProjects] = useState([]);
    const [loggedIn, setLoggedIn] = useContext(LoginContext);

    useEffect(() => {
        fetch('/all-projects').then(res => res.json()).then(json => {
            setProjectData(json);
            setFilteredProjects(Object.values(json));
        })
    }, []);

    return (
        <>
            <Container className="mt-3">
                { /* Search */ }
                { JSON.stringify(projectData) !== "{}" && <SearchBox {...projectData} updateFilter={setFilteredProjects} /> }

                { /* Projects */ }
                <Row className="g-4">
                    { /* --- All # projects --- */ }
                    <div className="d-flex justify-content-center pt-4">
                        <hr style={{ width: "100%", color: "grey", backgroundColor: "grey", height: 1 }} />
                        <h6 style={{ textAlign: "center", color: "grey", margin: "0 10px" }}>All {filteredProjects.length} Projects</h6>
                        <hr style={{ width: "100%", color: "grey", backgroundColor: "grey", height: 1 }} />
                    </div>
                    { /* List of projects */ }
                    {
                        filteredProjects.length > 0 && filteredProjects.map(project => (
                            <Col style={{ display: "flex" }} xs={12} sm={6} md={4} key={`${project.pUID}-${project.title}`}>
                                <Project {...project} />
                            </Col>
                        ))
                    }
                </Row>
            </Container>
        </>
    );
};

export default Home;

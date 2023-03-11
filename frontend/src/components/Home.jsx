import { useEffect, useState } from 'react';
import { Container, Row, Col } from "react-bootstrap";

import Project from './Project';
import SearchBox from './SearchBox';

import json from '../assets/sample_data/all-projects.json';

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [filteredProjects, setFilteredProjects] = useState([]);

    useEffect(() => {
        setProjectData(json);
    }, []);

    return (
        <>
            <Container className="mt-3">
                {
                    JSON.stringify(projectData) !== "{}" && <SearchBox {...projectData} updateFilter={setFilteredProjects}/>
                }
                <Row className="g-4">
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

import json from '../assets/sample_data/all-projects.json';

import Project from './Project';

import { useEffect, useState } from 'react';
import { Container, Form, Row, Col } from "react-bootstrap";

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        /*
        fetch(TODO).then(response => response.json()).then(data => {
            setProjectData(data);
        }).catch(err => console.log(err));
        */
        setProjectData(json);
    }, []);

    useEffect(() => {
        Object.values(projectData).map(value => {
            return(setProjects(oldProjects => [...oldProjects, value]));
        });
    }, [projectData]);

    // TODO: search functionality (Form)
 
    return (
        <Container fluid>
            <Row><h1>pigeonhole.dev</h1></Row>
            <Row className="g-4">
                {
                    projects.map(project => {
                        return (
                            <Col style={{ display: 'flex' }} xs={12} sm={6} md={4} key={project.pUID}> 
                                <Project {...project}/>
                            </Col>
                        );
                    })
                }
            </Row>
        </Container>
    );
}

export default Home;
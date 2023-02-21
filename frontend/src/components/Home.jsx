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
 
    return (
        <Container fluid>
            <Row>
                {
                    projects.map(project => {
                        return (
                            <Col xs={12} sm={6} md={4} lg={3} xl={2} key={project.pUID}>
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
import { useEffect, useState } from 'react';
import { Container, Row, Col } from "react-bootstrap";

import Project from './Project';
import SearchBox from './SearchBox';

import json from '../assets/sample_data/all-projects.json';

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [filteredProjects, setFilteredProjects] = useState([]);

    useEffect(() => {
        const fetchProjects = async () => {
          try {
            const res = await fetch('/all-projects');
            if (!res.ok) {
              throw new Error('Network response was not ok');
            }
            const data = await res.json();
            setProjectData(data);
            setFilteredProjects(Object.values(data));
          } catch (error) {
            console.log('Error:', error);
          }
        };
      
        fetchProjects();
      }, []);

    // From JSON
    // useEffect(() => {
        // setProjectData(json);
        // setFilteredProjects(Object.values(json));
    // }, []);

    return (
        <>
            <Container className="mt-3">
                {
                    JSON.stringify(projectData) !== "{}" && <SearchBox {...projectData} updateFilter={setFilteredProjects} />
                }
                <Row className="g-4">

                    <div className="d-flex justify-content-center pt-4">
                        <hr style={{ width: "100%", color: "grey", backgroundColor: "grey", height: 1 }} />
                        <h6 style={{ textAlign: "center", color: "grey", margin: "0 10px" }}>All {filteredProjects.length} Projects</h6>
                        <hr style={{ width: "100%", color: "grey", backgroundColor: "grey", height: 1 }} />
                    </div>

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

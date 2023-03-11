import { useEffect, useState } from 'react';
import { Container, Card, Form, Navbar, Nav, FormControl, Button, Row, Col } from "react-bootstrap";

import Project from './Project';
import SearchBox from './SearchBox';

import json from '../assets/sample_data/all-projects.json';

const Home = () => {
    const [projectData, setProjectData] = useState({});
    const [filteredProjects, setFilteredProjects] = useState([]);

    useEffect(() => {
        setProjectData(json);
    }, []);



{/*
    const getFilteredProjects = () => { // TODO: using filteredProjects, render all projects
        let newFilteredProjects = projects;

        const activeFilters = [...new Set([...topicFilters, ...issueFilters])];

        if (search) {
            newFilteredProjects = newFilteredProjects.filter((project) => {
                const gh_repo_name = project.gh_repo_name?.toLowerCase();
                const topics = Array.from({ length: 5 })
                    .flatMap((_, i) => project[`gh_topics_${i + 1}`])
                    .filter(Boolean);
                const matches = topics.some((topic) =>
                    topic.toLowerCase().includes(search)
                );
                return gh_repo_name.includes(search) && matches;
            });
        }

        if (activeFilters.length > 0) {
            newFilteredProjects = newFilteredProjects.filter((project) => {
                const matchedTopicFilters = topicFilters.every((topicFilter) => {
                    return Array.from({ length: 5 }).some(
                        (_, i) => project[`gh_topics_${i + 1}`] === topicFilter
                    );
                });

                const matchedIssueFilters = issueFilters.every((issueFilter) => {
                    return Array.from({ length: 7 }).some(
                        (_, i) => project[`issue_label_${i + 1}`] === issueFilter
                    );
                });

                return matchedTopicFilters && matchedIssueFilters;
            });

            // Ensure that only projects that match all activeFilters are returned
            activeFilters.forEach((filter) => {
                const isTopicFilter = topicFilters.includes(filter);
                const filterKey = isTopicFilter ? 'gh_topics' : 'issue_label';
                newFilteredProjects = newFilteredProjects.filter((project) => {
                    return Array.from({ length: 5 + (isTopicFilter ? 0 : 2) })
                        .some((_, i) => project[`${filterKey}_${i + 1}`] === filter ||
                            (isTopicFilter && i >= 5 && project[`gh_topics_${i + 1}`] === filter) ||
                            (!isTopicFilter && i >= 7 && project[`issue_label_${i + 1}`] === filter));
                });
            });
        }

        return newFilteredProjects;
    };
*/}



    return (
        <>
            <Container className="mt-3">
                {
                    JSON.stringify(projectData) !== "{}" && <SearchBox {...projectData}/> // TODO: pass a callback function into <SearchBox> to modify filteredProjects
                }
                <Row className="g-4">
                    {filteredProjects.map(project => (
                        <Col
                            style={{ display: "flex" }}
                            xs={12}
                            sm={6}
                            md={4}
                            key={`${project.pUID}-${project.title}`}
                        >
                            <Project {...project} />
                        </Col>
                    ))}
                </Row>
            </Container>
        </>
    );
};

export default Home;

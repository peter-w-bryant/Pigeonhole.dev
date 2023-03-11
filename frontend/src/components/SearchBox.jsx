import { useEffect, useState } from 'react';

import { Container, Card, Form, Navbar, Nav, FormControl, Button, Row, Col } from "react-bootstrap";

const SearchBox = (props) => {
    const [projects, setProjects] = useState([]);

    const [topics, setTopics] = useState([]);
    const [issues, setIssues] = useState([]);




    

    const [searchTerm, setSearchTerm] = useState('');
    const [filteredProjects, setFilteredProjects] = useState([]);
    const [topicFilters, setTopicFilters] = useState([]);
    const [issueFilters, setIssueFilters] = useState([]);

    useEffect(() => {
        const projectList = Object.values(props); 
        setProjects(projectList);
        setFilteredProjects(projectList);
    }, []);

    useEffect(() => {
        Array.from({ length: 5 }).map((_, i) => {
            const topics = projects.map(project => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const uniqueTopics = [...new Set(topics)];
            uniqueTopics.map(topic => {
                setTopics(oldTopics => [...oldTopics, topic])
            });
        });
        Array.from({ length: 7 }).map((_, i) => {
            const issues = projects.map(project => project[`issue_label_${i + 1}`]).filter(Boolean);
            const uniqueIssues = [...new Set(issues)];
            uniqueIssues.map(issue => {
                setIssues(oldIssues => [...oldIssues, issue])
            });
        })
    }, [projects]); 





    const handleSearch = (event) => {
        const searchTerm = event.target.value.toLowerCase();
        if (event.key === "Backspace" || event.keyCode === 8) {
            // If backspace key is pressed, filter projects based on updated search substring
            const newFilteredProjects = projects.filter(project => {
                const gh_repo_name = project.gh_repo_name?.toLowerCase();
                const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
                const matches = topics.some(topic => topic.toLowerCase().includes(searchTerm));
                const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
                const issueMatches = issues.some(issue => issue.toLowerCase().includes(searchTerm));
                return gh_repo_name.includes(searchTerm) || matches || issueMatches;
            });
            setFilteredProjects(newFilteredProjects);
        } else {
            const newFilteredProjects = searchTerm ? projects.filter(project => {
                const gh_repo_name = project.gh_repo_name?.toLowerCase();
                const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
                const matches = topics.some(topic => topic.toLowerCase().includes(searchTerm));
                const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
                const issueMatches = issues.some(issue => issue.toLowerCase().includes(searchTerm));
                return gh_repo_name.includes(searchTerm) || matches || issueMatches;
            }) : projects;
            setFilteredProjects(newFilteredProjects);
        }
        setSearchTerm(searchTerm);
    };


    const handleTopicFilter = (event) => {
        const topic = event.target.value;
        if (topic) {
            setTopicFilters((prevFilters) => [...prevFilters, topic]);
            const newFilteredProjects = projects.filter(project =>
                Array.from({ length: 5 }).some((_, i) => project[`gh_topics_${i + 1}`] === topic)
            );
            setFilteredProjects(newFilteredProjects);
        } else {
            setTopicFilters([]);
            setFilteredProjects(getFilteredProjects(issueFilters, []));
        }
    };

    const handleIssueFilter = (event) => {
        const issue = event.target.value;
        if (issue) {
            setIssueFilters((prevFilters) => [...prevFilters, issue]);
            const newFilteredProjects = projects.filter(project =>
                Array.from({ length: 7 }).some((_, i) => project[`issue_label_${i + 1}`] === issue)
            );
            setFilteredProjects(newFilteredProjects);
        } else {
            setIssueFilters([]);
            setFilteredProjects(getFilteredProjects([], topicFilters));
        }
    };

    const getFilteredProjects = () => {
        let newFilteredProjects = projects;

        const activeFilters = [...new Set([...topicFilters, ...issueFilters])];

        if (searchTerm) {
            newFilteredProjects = newFilteredProjects.filter((project) => {
                const gh_repo_name = project.gh_repo_name?.toLowerCase();
                const topics = Array.from({ length: 5 })
                    .flatMap((_, i) => project[`gh_topics_${i + 1}`])
                    .filter(Boolean);
                const matches = topics.some((topic) =>
                    topic.toLowerCase().includes(searchTerm)
                );
                return gh_repo_name.includes(searchTerm) && matches;
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

    const handleClearFilter = (filter) => {
        setTopicFilters([]);
        setIssueFilters([]);
        setFilteredProjects(projects);
        setSearchTerm('');
    };

    const activeFilters = [...topicFilters, ...issueFilters].map(filter => (
        <span key={filter} className="badge rounded-pill bg-secondary me-2">{filter} <i className="bi bi-x-circle" onClick={() => handleClearFilter(filter)}></i></span>
    ));

    return (
        <>
            <Container className="mt-3">
                <Row className="justify-content-center">
                    <Col md={6}>
                        <Card>
                            <Card.Body>
                                <Form className="d-flex">
                                    <FormControl
                                        placeholder="Search projects by keyword"
                                        value={searchTerm}
                                        onChange={handleSearch}
                                        style={{ paddingBottom: "0.5rem" }}
                                    />
                                </Form>
                                <br />
                                <h5>Filter</h5>
                                <Form>
                                    <Row>
                                        <Col xs={6}>
                                            <h6>By topics</h6>
                                            <Form.Select
                                                className="mb-2"
                                                aria-label="Filter by topics"
                                                value={topicFilters}
                                                onChange={handleTopicFilter} 
                                                multiple> { topics.map(topic => <option key={topic}>{topic}</option>) }
                                            </Form.Select>
                                        </Col>
                                        <Col xs={6}>
                                            <h6>By issues</h6>
                                            <Form.Select
                                                className="mb-2"
                                                aria-label="Filter by issues"
                                                title='Filter by issues'
                                                value={issueFilters}
                                                onChange={handleIssueFilter}
                                                multiple>
                                                { issues.map(issue => <option key={issue}>{issue}</option>) }
                                            </Form.Select>
                                        </Col>  
                                    </Row>
                                    <Card.Footer>
                                        {
                                            activeFilters.length > 0 && (
                                                <Row className="mb-2">
                                                    <h6>Active Filters:</h6>
                                                    {activeFilters}
                                                    <Button className="ms-2" variant="secondary" size="sm" onClick={handleClearFilter}>
                                                        Clear Filters
                                                    </Button>
                                                </Row>
                                            )
                                        }
                                    </Card.Footer>
                                </Form>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    );
};

export default SearchBox;
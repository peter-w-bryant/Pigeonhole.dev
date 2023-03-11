import { useEffect, useState } from 'react';

import { Container, Card, Form, Navbar, Nav, FormControl, Button, Row, Col } from "react-bootstrap";

const SearchBox = (props) => {
    const [projects, setProjects] = useState([]);

    const [search, setSearch] = useState('');
    const [topics, setTopics] = useState([]);
    const [issues, setIssues] = useState([]);

    const [searchFilters, setSearchFilters] = useState([]);
    const [topicFilters, setTopicFilters] = useState([]);
    const [issueFilters, setIssueFilters] = useState([]);

    useEffect(() => {
        const projectList = Object.values(props); 
        setProjects(projectList);
    }, []);

    useEffect(() => {
        Array.from({ length: 5 }).map((_, i) => {
            const topics = projects.map(project => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const uniqueTopics = [...new Set(topics)];
            setTopics(uniqueTopics);
        });
        Array.from({ length: 7 }).map((_, i) => {
            const issues = projects.map(project => project[`issue_label_${i + 1}`]).filter(Boolean);
            const uniqueIssues = [...new Set(issues)];
            setIssues(uniqueIssues);
        })
    }, [projects]); 

    const handleClearFilter = () => {
        setSearch('');
        setSearchFilters([]);
        setTopicFilters([]);
        setIssueFilters([]);
        setFilteredProjects(projects);
    };

    const handleSearch = (event) => {
        setSearch(event.target.value.toLowerCase());
        handleSearchFilter();
    }

    const handleSearchFilter = () => {
        const filtered = projects.filter(project => {
            const gh_repo_name = project.gh_repo_name.toLowerCase();

            const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const topicMatches = topics.some(topic => topic.toLowerCase().includes(search));

            const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
            const issueMatches = issues.some(issue => issue.toLowerCase().includes(search));

            return gh_repo_name.includes(search) || topicMatches || issueMatches;
        });
        setSearchFilters(filtered);
    };



    const handleTopicFilter = (event) => { // TODO: revamp this function
        /*
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
        */
    };

    const handleIssueFilter = (event) => { // TODO: revamp this function
        /*
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
        */
    };

    const activeFilters = [...topicFilters, ...issueFilters].map(filter => ( // TODO: make activeFilters looks better (solution may be in return function)
        <span key={filter} className="badge rounded-pill bg-secondary me-2">{filter} <i className="bi bi-x-circle" onClick={() => handleClearFilter(filter)}></i></span>
    ));

    // TODO: using the three filtered lists and the callback function, alter filteredProjects in ./Home




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
                                        value={search}
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
                                                multiple> { topics.map(topic => <option key={`topic${topics.indexOf(topic)}-${topic}`}>{topic}</option>) } {/* TODO: create better keys */}
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
                                                { issues.map(issue => <option key={`issue${issues.indexOf(issue)}-${issue}`}>{issue}</option>) } {/* TODO: create better keys */}
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
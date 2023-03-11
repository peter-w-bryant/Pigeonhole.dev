import { useEffect, useState } from 'react';
import { Container, Card, Form, FormControl, Button, Row, Col } from "react-bootstrap";
import { AiOutlineCloseCircle } from 'react-icons/ai'

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
    }, [props]);

    useEffect(() => {
        /* TODO: generate final filtered list (currently does not work, need to check functionality of filters)
        const filtered = searchFilters.filter(project => {
            let isFiltered = false;
            Array.from({ length: 5 }).map((_, i) => {
                const topic = project[`gh_topics_${i + 1}`];
                return topic !== "" && (isFiltered = true);
            });
            return isFiltered;
        }).filter(project => { 
            let isFiltered = false;
            Array.from({ length: 7 }).map((_, i) => {
                const issue = project[`issue_label_${i + 1}`];
                return issue !== "" && (isFiltered = true);
            });
            return isFiltered;
        });
        console.log(filtered)
        handleUpdate(filtered);
        */
    }, [searchFilters, topicFilters, issueFilters]);

    useEffect(() => {
        Array.from({ length: 5 }).map((_, i) => { // NOTE: gh_topics starts at 0, is this intentional?
            const topics = projects.map(project => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const uniqueTopics = [...new Set(topics)];
            return setTopics(uniqueTopics);
        });
        Array.from({ length: 7 }).map((_, i) => {
            const issues = projects.map(project => project[`issue_label_${i + 1}`]).filter(Boolean);
            const uniqueIssues = [...new Set(issues)];
            return setIssues(uniqueIssues);
        })
    }, [projects]); 

    const handleUpdate = (filtered) => {
        props.updateFilter(filtered); 
    };

    const handleClearFilter = () => {
        setSearch('');
        setSearchFilters([]);
        setTopicFilters([]);
        setIssueFilters([]);
    };

    const handleSearch = (event) => {
        setSearch(event.target.value.toLowerCase());
        handleSearchFilter();
    }

    const handleSearchFilter = () => {
        const filtered = projects.filter(project => {
            const gh_repo_name = project.gh_repo_name?.toLowerCase();

            const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const topicMatches = topics.some(topic => topic.toLowerCase().includes(search));

            const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
            const issueMatches = issues.some(issue => issue.toLowerCase().includes(search));

            return gh_repo_name?.includes(search) || topicMatches || issueMatches;
        });
        setSearchFilters(filtered);
    };

    const handleTopicFilter = (event) => {
        const topic = event.target.value;
        setTopicFilters(oldFilters => {
            return !oldFilters.includes(topic) ? [...oldFilters, topic] : [...oldFilters]
        });
    };

    const handleIssueFilter = (event) => {
        const issue = event.target.value;
        setIssueFilters(oldFilters => {
            return !oldFilters.includes(issue) ? [...oldFilters, issue] : [...oldFilters]
        });
    };

    const handleRemoveFilter = (filter) => {
        topicFilters.includes(filter) ? setTopicFilters(
            oldFilters => oldFilters.filter(oldFilter => oldFilter !== filter)
        ) : setIssueFilters(
            oldFilters => oldFilters.filter(oldFilter => oldFilter !== filter)
        );
    };

    const activeFilters = [...topicFilters, ...issueFilters].map(filter => (
        <Col key={filter} className="badge rounded-pill bg-secondary me-2">{filter}   <AiOutlineCloseCircle onClick={() => handleRemoveFilter(filter)} /></Col>
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
                                                    <Button className="mt-2" variant="secondary" size="sm" onClick={handleClearFilter}>
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
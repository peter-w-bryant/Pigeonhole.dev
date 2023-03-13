import { useCallback, useEffect, useState } from 'react';
import { Container, Card, Form, FormControl, Button, Row, Col, Dropdown } from "react-bootstrap";
import { AiOutlineCloseCircle } from 'react-icons/ai'

const SearchBox = (props) => {
    const [projects, setProjects] = useState([]);

    const [topics, setTopics] = useState([]);
    const [issues, setIssues] = useState([]);

    const [search, setSearch] = useState('');
    const [topicFilters, setTopicFilters] = useState([]);
    const [issueFilters, setIssueFilters] = useState([]);

    const [final, setFinal] = useState([]);

    useEffect(() => {
        const projectList = Object.values(props);
        setProjects(projectList);
    }, [props]);

    useEffect(() => {
        const allTopics = [];
        const allIssues = [];

        Array.from({ length: 5 }).forEach((_, i) => { // NOTE: gh_topics starts at 0, is this intentional?
            const topics = projects.map(project => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const uniqueTopics = [...new Set(topics)];
            allTopics.push(...uniqueTopics);
        });

        Array.from({ length: 7 }).forEach((_, i) => {
            const issues = projects.map(project => project[`issue_label_${i + 1}`]).filter(Boolean);
            const uniqueIssues = [...new Set(issues)];
            allIssues.push(...uniqueIssues);
        });

        setTopics(Array.from(new Set(allTopics)));
        setIssues(Array.from(new Set(allIssues)));
    }, [projects]);

    const filterSearch = useCallback(() => {
        const filtered = projects.filter(project => {
            const gh_repo_name = project.gh_repo_name?.toLowerCase();

            const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
            const topicMatches = topics.some(topic => topic.toLowerCase().includes(search));

            const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
            const issueMatches = issues.some(issue => issue.toLowerCase().includes(search));

            return gh_repo_name?.includes(search) || topicMatches || issueMatches;
        });
        return filtered;
    }, [projects, search]);

    useEffect(() => { // NOTE: currently, filtering is done like so: search AND (topic or topic or topic) AND (issue or issue or issue)
        const filtered = filterSearch().filter(project => {
            let isFiltered = false;
            Array.from({ length: 5 }).map((_, i) => {
                const topic = project[`gh_topics_${i + 1}`];
                topicFilters.length === 0 ? (isFiltered = true) : (topic !== "" && topicFilters.includes(topic)) && (isFiltered = true);
                return isFiltered;
            });
            return isFiltered;
        }).filter(project => {
            let isFiltered = false;
            Array.from({ length: 7 }).map((_, i) => {
                const issue = project[`issue_label_${i + 1}`];
                issueFilters.length === 0 ? (isFiltered = true) : (issue !== "" && issueFilters.includes(issue)) && (isFiltered = true)
                return isFiltered;
            });
            return isFiltered;
        });
        setFinal(filtered);
    }, [topicFilters, issueFilters, filterSearch]); // TODO: filterSearch and handleUpdate causing maximum depth update reached

    const handleSearch = (event) => {
        setSearch(event.target.value.toLowerCase());
    }

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

    const handleClearFilter = () => {
        setSearch('');
        setTopicFilters([]);
        setIssueFilters([]);
    };

    const handleUpdate = (event) => {
        event.preventDefault();
        props.updateFilter(final);
    };

    const activeFilters = [...topicFilters, ...issueFilters].map(filter => {
        const truncatedFilter = filter.length > 5 ? `${filter.slice(0, 5)}...` : filter;
        return (
            <Col key={filter} className="badge rounded-pill bg-secondary me-2" title={filter}>
                {truncatedFilter} <AiOutlineCloseCircle onClick={() => handleRemoveFilter(filter)} />
            </Col>
        );
    });

    return (
        <>
            <Container className="mt-3">
                <Row>
                    <FormControl
                        placeholder="Search projects by keyword 🔍"
                        value={search}
                        onChange={handleSearch}
                        style={{ paddingBottom: "0.5rem" }}
                    />
                </Row>
                <Row>
                    <table>
                        <tbody className="d-flex flex-row">
                        <tr>
                            <td>
                                <Dropdown>
                                    <Dropdown.Toggle variant={topicFilters.length > 0 ? "primary" : "outline-dark"} id="topic-dropdown">
                                        {topicFilters.length > 0 ? (
                                            <>
                                                {topicFilters.slice(0, 1)}
                                                {topicFilters.length > 1 && ` and ${topicFilters.length - 1} other`}
                                            </>
                                        ) : (
                                            "Topics"
                                        )}
                                    </Dropdown.Toggle>
                                    <Dropdown.Menu style={{ maxHeight: "200px", overflowY: "auto" }}>
                                        <Form.Group>
                                            {topics.map((topic) => (
                                                <Form.Check
                                                    key={`topic${topics.indexOf(topic)}-${topic}`}
                                                    type="checkbox"
                                                    label={topic}
                                                    value={topic}
                                                    checked={topicFilters.includes(topic)}
                                                    onChange={handleTopicFilter}
                                                />
                                            ))}
                                        </Form.Group>
                                    </Dropdown.Menu>
                                </Dropdown>
                            </td>
                            <td>
                                <Dropdown>
                                    <Dropdown.Toggle variant={issueFilters.length > 0 ? "primary" : "outline-dark"} id="issue-dropdown">
                                        {issueFilters.length > 0 ? (
                                            <>
                                                {issueFilters.slice(0, 1)}
                                                {issueFilters.length > 1 && ` and ${issueFilters.length - 1} other`}
                                            </>
                                        ) : (
                                            "Issues"
                                        )}
                                    </Dropdown.Toggle>
                                    <Dropdown.Menu style={{ maxHeight: "200px", overflowY: "auto" }}>
                                        <Form.Group>
                                            {issues.map((issue) => (
                                                <Form.Check
                                                    key={`issue${issues.indexOf(issue)}-${issue}`}
                                                    type="checkbox"
                                                    label={issue}
                                                    value={issue}
                                                    checked={issueFilters.includes(issue)}
                                                    onChange={handleIssueFilter}
                                                />
                                            ))}
                                        </Form.Group>
                                    </Dropdown.Menu>
                                </Dropdown>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                        <Col className="p-0">
                            <Button className="mb-2 mt-1" variant="outline-primary" onClick={handleUpdate}>
                                Search
                            </Button>
                            {(search !== "" || activeFilters.length > 0) && (
                                <Card.Footer>
                                    <Button className="mt-2" variant="secondary" size="sm" onClick={handleClearFilter}>
                                        Clear Filters
                                    </Button>
                                </Card.Footer>
                            )}
                        </Col>
                </Row>
            </Container>

        </>

    );
};

export default SearchBox;
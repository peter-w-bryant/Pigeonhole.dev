import { useCallback, useEffect, useState } from 'react';
import { Container, Card, Form, FormControl, Button, Row, Col, Dropdown } from "react-bootstrap";
import { AiOutlineCloseCircle } from 'react-icons/ai'

// import Project from './Project';
import Project from './Project';

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

    useEffect(() => {
        const filterSearch = () => {
            const filtered = projects.filter(project => {
                const gh_repo_name = project.gh_repo_name?.toLowerCase();

                const topics = Array.from({ length: 5 }).flatMap((_, i) => project[`gh_topics_${i + 1}`]).filter(Boolean);
                const topicMatches = topics.some(topic => topic.toLowerCase().includes(search));

                const issues = Array.from({ length: 7 }).flatMap((_, i) => project[`issue_label_${i + 1}`]).filter(Boolean);
                const issueMatches = issues.some(issue => issue.toLowerCase().includes(search));

                return gh_repo_name?.includes(search) || topicMatches || issueMatches;
            });
            return filtered;
        };

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
    }, [projects, search, topicFilters, issueFilters]);

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
                <Row style={{ paddingTop: "0.2rem", paddingBottom: "0.2rem" }}>
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
                                {(search !== "" || activeFilters.length > 0) && (
                                    <td>
                                        <Button variant="outline-danger" onClick={handleClearFilter}>
                                            Clear Filters
                                        </Button>
                                    </td>

                                )}
                                <td>
                                    <Button variant="outline-primary" onClick={handleUpdate}>
                                        Search
                                    </Button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </Row>
            </Container>

            <Container className="mt-3">
                {final.length === 0 ? (
                    <Row>
                        <Col>No results found</Col>
                    </Row>
                ) : (
                    (search === "" && topicFilters.length === 0 && issueFilters.length === 0) ? (
                        <>
                        </>
                    ) : (
                        <Row xs={1} sm={2} md={3}>
                            {final.map((project) => (
                                <Col style={{ display: "flex" }} key={`${project.pUID}-${project.title}`}>
                                    <Project {...project} />
                                </Col>
                            ))}
                        </Row>
                    )
                )}
            </Container>


            <Container className="mt-3">
                <Row>
                    {activeFilters.length > 0 && (
                        <>
                            <Col>
                                <div>Active Filters:</div>
                                <div className="d-flex flex-wrap">{activeFilters}</div>
                            </Col>
                        </>
                    )}
                </Row>
            </Container>
        </>
    );

}

export default SearchBox;
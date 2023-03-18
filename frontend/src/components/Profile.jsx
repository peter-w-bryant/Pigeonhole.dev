import { useState, useEffect, useContext } from 'react';
import { Container, Card, Form, FormControl, Button, Row, Col, Dropdown } from "react-bootstrap";
import LoginContext from '../contexts/loginContext';
import Project from './Project';

const Profile = () => {

    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [savedProjects, setSavedProjects] = useState([]);
    const [allProjects, setAllProjects] = useState([]);

    const handleUnsaveAllClick = async () => {
        try {
            const res = await fetch('/delete-all-projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: loggedIn
                })
            });
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await res.json();

            // Update saved projects list
            setSavedProjects([]);

            alert(data['success']);
        } catch (error) {
            console.log('Error:', error);
        }
    };

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const res = await fetch('/all-projects');
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await res.json();
                setAllProjects(Object.values(data));
            } catch (error) {
                console.log('Error:', error);
            }
        };

        fetchProjects();
    }, []);

    useEffect(() => {
        const fetchSavedProjects = async () => {
            try {
                const res = await fetch(`/saved-projects/${loggedIn}`);
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await res.json();
                console.log(Object.values(data['projects']))
                setSavedProjects(Object.values(data['projects']));
            } catch (error) {
                console.log('Error:', error);
            }
        };

        if (loggedIn !== '') {
            fetchSavedProjects();
        }
    }, [loggedIn]);

    return (
        <>
            <Container className="mt-3">

                <div>
                    <h2>Saved Projects</h2>
                    <Button variant="outline-danger" onClick={handleUnsaveAllClick}>
                        Unsave All
                    </Button>

                    {savedProjects.length === 0 && (
                        <p>No saved projects.</p>
                    )}
                    {savedProjects.length > 0 && (

                        <Row xs={1} sm={2} md={3}>
                            {savedProjects.map(project => (
                                <Col style={{ display: "flex", marginBottom: "16px" }} key={`${project.pUID}-${project.title}`}>
                                    <Project {...project} />
                                </Col>
                            ))}
                        </Row>
                    )}
                </div>
            </Container>
        </>
    );
};

export default Profile;

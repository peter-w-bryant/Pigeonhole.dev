import { useState, useEffect, useContext } from 'react';
import { Container, Button, Row, Col } from "react-bootstrap";

import { FaHtml5, FaCss3Alt, FaJs, FaPython, FaJava, FaPhp, FaSwift, FaAngular, FaReact, FaVuejs, FaNodeJs, FaBootstrap, FaSass, FaLess, } from 'react-icons/fa'

import Project from './Project';

import LoginContext from '../contexts/loginContext';

const Profile = () => {

    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [savedProjects, setSavedProjects] = useState([]);

    useEffect(() => {
        loggedIn !== '' ? (
            fetch('/saved-projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "username": loggedIn })
            }).then(res => res.json()).then(json => {
                setSavedProjects(Object.values(json['projects']));
            })
        ) : setSavedProjects([]);
      
    }, [loggedIn]);
      
    const handleUnsaveAllClick = () => {
        fetch('/delete-all-projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: loggedIn
            })
        }).then(res => res.json()).then(json => {
            setSavedProjects([]);
            alert(json['success'])
        });
    };

    return (
        <>
            <Container className="mt-3">
                <h2> {loggedIn}'s Profile </h2>

                <br />
                
                { /* Skills */ }
                <Row>
                    <h3 style={{textAlign: "center"}}>Skills</h3>
                    <div style={{display: "flex", justifyContent: "center"}}>
                        <h4 style={{marginRight: "10px"}}>Languages</h4>
                        <Button variant="outline-primary">
                            <FaHtml5 />
                            &nbsp; HTML
                        </Button>
                        <Button variant="outline-primary">
                            <FaCss3Alt />
                            &nbsp; CSS
                        </Button>
                        <Button variant="outline-primary">
                            <FaJs />
                            &nbsp; JavaScript
                        </Button>
                        <Button variant="outline-primary">
                            <FaPython />
                            &nbsp; Python
                        </Button>
                        <Button variant="outline-primary">
                            <FaJava />
                            &nbsp; Java
                        </Button>
                        
                        
                        <Button variant="outline-primary">
                            <FaPhp />
                            &nbsp; PHP
                        </Button>
                        <Button variant="outline-primary">
                            <FaSwift />
                            &nbsp; Swift
                        </Button>
                       
                    </div>
                    <div style={{display: "flex", justifyContent: "center"}}>
                        <h4 style={{marginRight: "10px"}}>Frameworks/Libraries</h4>
                        <Button variant="outline-primary">
                            <FaReact />
                            &nbsp; React
                        </Button>
                        <Button variant="outline-primary">
                            <FaAngular />
                            &nbsp; Angular
                        </Button>
                        <Button variant="outline-primary">
                            <FaVuejs />
                            &nbsp; Vue.js
                        </Button>
                        <Button variant="outline-primary">
                            <FaNodeJs />
                            &nbsp; Node.js
                        </Button>
                        <Button variant="outline-primary">
                            <FaBootstrap />
                            &nbsp; Bootstrap
                        </Button>
                        <Button variant="outline-primary">
                            <FaSass />
                            &nbsp; Sass
                        </Button>
                        <Button variant="outline-primary">
                            <FaLess />
                            &nbsp; Less
                        </Button>
                    </div>
                </Row>

                { /* Saved Projects */ }
                <Row><Container>
                    <h3>Saved Projects ({savedProjects.length})</h3>
                    <Button variant="outline-danger" onClick={handleUnsaveAllClick} style={{ float: "right" }}>
                        Unsave All
                    </Button>

                    <br /> <br />

                    { savedProjects.length === 0 ? (<p>No saved projects.</p>) : (
                            <Row xs={1} sm={2} md={3}>
                                {savedProjects.map(project => (
                                    <Col style={{ display: "flex", marginBottom: "16px" }} key={`${project.pUID}-${project.title}`}>
                                        <Project {...project} />
                                    </Col>
                                ))}
                            </Row>
                        )
                    }
                </Container></Row>
            </Container>
        </>
    );
};

export default Profile;

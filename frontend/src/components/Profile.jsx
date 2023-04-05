import { useState, useEffect, useContext } from 'react';
import { Container, Card, Form, FormControl, Button, Row, Col, Dropdown } from "react-bootstrap";
import LoginContext from '../contexts/loginContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faHtml5, 
    faCss3Alt, 
    faJs, 
    faPython, 
    faJava, 
    faPhp, 
    faSwift, 
    faCodeBranch, 
    faRProject, 
    faDart,
    faCaretSquareRight,
    faAngular,
    faReact,
    faVuejs,
    faNodeJs,
    faBootstrap,
    faSass,
    faLess,
    faJquery,
    faTypescript,
    faCSharp,
    faRuby
} from '@fortawesome/free-brands-svg-icons';
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
            const res = await fetch('/saved-projects', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ "username": loggedIn })
            });
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
                <h2> {loggedIn}'s Profile </h2>

                <br />

                <div>
                    <div>
                        <div>
                        <h3 style={{textAlign: "center"}}>Skills</h3>

                        <div style={{display: "flex", justifyContent: "center"}}>
                            <h4 style={{marginRight: "10px"}}>Languages</h4>

                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faHtml5} />
                                &nbsp; HTML
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faCss3Alt} />
                                &nbsp; CSS
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faJs} />
                                &nbsp; JavaScript
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faPython} />
                                &nbsp; Python
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faJava} />
                                &nbsp; Java
                            </Button>
                            
                            
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faPhp} />
                                &nbsp; PHP
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faSwift} />
                                &nbsp; Swift
                            </Button>
                           
                        </div>

                        <div style={{display: "flex", justifyContent: "center"}}>
                            <h4 style={{marginRight: "10px"}}>Frameworks/Libraries</h4>

                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faReact} />
                                &nbsp; React
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faAngular} />
                                &nbsp; Angular
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faVuejs} />
                                &nbsp; Vue.js
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faNodeJs} />
                                &nbsp; Node.js
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faBootstrap} />
                                &nbsp; Bootstrap
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faSass} />
                                &nbsp; Sass
                            </Button>
                            <Button variant="outline-primary">
                                <FontAwesomeIcon icon={faLess} />
                                &nbsp; Less
                            </Button>
                          
                        </div>
                    </div>

                    <br />
                    </div>




                </div>
                <div>
                    <h3>Saved Projects ({savedProjects.length})</h3>

                    <Button variant="outline-danger" onClick={handleUnsaveAllClick} style={{ float: "right" }}>
                        Unsave All
                    </Button>
                    <br /> <br />

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

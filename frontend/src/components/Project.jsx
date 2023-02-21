/* eslint-disable jsx-a11y/anchor-has-content */


import { Card, ListGroup } from 'react-bootstrap';
import { AiOutlineStar, AiOutlineFork, AiOutlineEye } from 'react-icons/ai'
import { FaGithub } from "react-icons/fa";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Project = (props) => {
    return (
        <Card bg='light'>
            <Card.Body >
                <div style={{ paddingBottom: '20px' }} >
                    <Card.Title>{props.gh_repo_name}<span className="float-end">
                        <FaGithub />
                    </span></Card.Title>
                    <Card.Subtitle className='mb-1 small' style={{ color: '#007BFF' }}>{props.gh_username}</Card.Subtitle>

                    <Card.Subtitle className='mb-2 text-muted small'><AiOutlineEye /> {props.num_watchers}&nbsp;<AiOutlineFork /> {props.num_forks}&nbsp;<AiOutlineStar /> {props.num_stars}</Card.Subtitle>

                    <Card.Text className="small">{props.gh_description}</Card.Text>
                </div>

                <div>
                    <Card.Subtitle className='mb-1 text-muted small'>Topics:</Card.Subtitle>
                    <ListGroup horizontal
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            listStyle: 'none',
                            fontSize: '0.5rem',
                            padding: '0',
                            margin: '0',
                        }}>
                        {[1, 2, 3, 4, 5].map(index => (
                            props[`gh_topics_${index}`] !== "" && (
                                <ListGroup.Item
                                    key={index}
                                    style={{
                                        height: 'fit-content',
                                        width: 'fit-content',
                                        borderRadius: '50px',
                                        backgroundColor: '#007BFF',
                                        color: '#ffffff',
                                        padding: '5px 10px',
                                        margin: '5px',
                                    }}>
                                    {props[`gh_topics_${index}`]}
                                </ListGroup.Item>
                            )
                        ))}
                    </ListGroup>
                </div>

                {/* <div >
                    <Card.Subtitle className='mb-1 text-muted small'>Open Issue Tags:</Card.Subtitle>
                    <ListGroup horizontal
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            listStyle: 'none',
                            fontSize: '0.5rem',
                            padding: '0',
                            margin: '0',
                        }}>
                        {[1, 2, 3].map(index => (
                            props[`issue_label_${index}`] !== "" && (
                                <ListGroup.Item 
                                    key={index}
                                    style={{
                                        height: 'fit-content',
                                        width: 'fit-content',
                                        borderRadius: '50px',
                                        backgroundColor: '#6c757d',
                                        color: '#ffffff',
                                        padding: '5px 10px',
                                        margin: '5px',
                                    }}>
                                    {props[`issue_label_${index}`]}
                                </ListGroup.Item>
                            )
                        ))}
                    </ListGroup> */}

                {/* </div> */}


                <a href={props.gh_rep_url} class="stretched-link"></a>
            </Card.Body>
            <Card.Footer>
                <small className='text-muted small' style={{fontSize: '0.8 rem', padding: '0'}}>Last commit: {props.date_last_commit}<br></br>
                Last merged PR: {props.date_last_merged_PR}</small>
            </Card.Footer>
        </Card>
    );
}

export default Project;
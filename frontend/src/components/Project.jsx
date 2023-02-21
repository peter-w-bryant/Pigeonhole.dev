/* eslint-disable jsx-a11y/anchor-has-content */

import Card from 'react-bootstrap/Card';
import { AiOutlineStar, AiOutlineFork, AiOutlineEye } from 'react-icons/ai'
import ListGroup from 'react-bootstrap/ListGroup';
import { FaGithub } from "react-icons/fa";

const Project = (props) => {
    return (
        <Card bg='light'>
            <Card.Body style={{ position: 'relative' }}>
                <div style={{ paddingBottom: '10px' }} >
                    <Card.Title>{props.gh_repo_name}</Card.Title>
                    <Card.Subtitle className='mb-2 text-muted'><AiOutlineEye /> {props.num_watchers}&emsp;<AiOutlineFork /> {props.num_forks}&emsp;<AiOutlineStar /> {props.num_stars}</Card.Subtitle>
                    <Card.Text>{props.gh_description}</Card.Text>
                </div>
                <div style={{ bottom: '0' }}>
                    <Card.Subtitle className='mb-1 text-muted small'>Open Issue Tags:</Card.Subtitle>
                    <ListGroup horizontal
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            listStyle: 'none',
                            padding: '0',
                            margin: '0',
                        }}>
                        {[1, 2, 3].map(index => (
                            props[`issue_label_${index}`] !== "" && (
                                <ListGroup.Item className='small'
                                    key={index}
                                    style={{
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
                    </ListGroup>
                </div>


                <a href={props.gh_rep_url} class="stretched-link"></a>
            </Card.Body>
            <Card.Footer>
                <small className='text-muted'>Last commit: {props.date_last_commit}</small>
                <span className="float-end">
                    <FaGithub />
                </span>
            </Card.Footer>
        </Card>
    );
}

export default Project;
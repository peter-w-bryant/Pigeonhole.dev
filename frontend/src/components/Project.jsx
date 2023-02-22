/* eslint-disable jsx-a11y/anchor-has-content */

import { Card, ListGroup } from 'react-bootstrap';
import { AiOutlineStar, AiOutlineFork, AiOutlineEye, AiOutlineCopyright, AiOutlineGithub} from 'react-icons/ai'

const Project = (props) => {
    return (
        <Card bg='light' style={{ width: '100%' }}>
            <Card.Body >
                <div style={{ paddingBottom: '20px' }} >
                    <Card.Title>{props.gh_repo_name}<span className="float-end">
                        <AiOutlineGithub />
                    </span></Card.Title>
                    <Card.Subtitle className='mb-1 small' style={{ color: '#007BFF' }}>{props.gh_username}</Card.Subtitle>

                    <Card.Subtitle className='mb-2 text-muted small'><AiOutlineEye /> {props.num_watchers}&nbsp;<AiOutlineFork /> {props.num_forks}&nbsp;<AiOutlineStar /> {props.num_stars}</Card.Subtitle>

                    <Card.Text className="small">{props.gh_description}</Card.Text>
                </div>

                <div style={{ paddingBottom: '10px' }}>
                    <Card.Subtitle className='mb-1 text-muted small'>Topics:</Card.Subtitle>
                    <ListGroup horizontal
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            listStyle: 'none',
                            fontSize: '0.75rem',
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
                <Card.Subtitle className='mb-1 text-muted small' style={{ background: 'transparent', border: 'none' }}>Issue Labels:</Card.Subtitle>



                <ListGroup horizontal
                    style={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        listStyle: 'none',
                        fontSize: '0.75rem',
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
                </ListGroup>
                {/* create a green heading that says Pigeonhole Score with the trademark */}
                <div style={{ paddingTop: '10px' }}>

                    <Card.Text className="small" style={{ fontSize: '0.6rem', fontWeight: 'bold' }}>Pigeonhole<br></br>New Contributor Score&nbsp;

                        <AiOutlineCopyright />:

                    </Card.Text>

                </div>
                <a href={props.gh_rep_url} className="stretched-link"></a>
            </Card.Body>
            <Card.Footer>
                <small className='text-muted float-start' style={{ fontSize: '0.8 rem', padding: '0' }}>Last commit: {props.date_last_commit}</small>
                <small className='text-muted float-end' style={{ fontSize: '0.8 rem', padding: '0' }}>Last merged PR: {props.date_last_merged_PR}</small>
            </Card.Footer>
        </Card >
    );
}

export default Project;
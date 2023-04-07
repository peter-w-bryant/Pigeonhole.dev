/* eslint-disable jsx-a11y/anchor-has-content */

import { useContext, useEffect, useState } from 'react';
import { Card, ListGroup } from 'react-bootstrap';

import { AiOutlineStar, AiOutlineFork, AiOutlineEye, AiOutlineCopyright, AiOutlineGithub, AiFillStar, AiOutlineCloseCircle } from 'react-icons/ai'
import { ToastContainer, toast } from 'react-toastify';

import LoginContext from "../contexts/loginContext";

import 'react-toastify/dist/ReactToastify.css';

const Project = (props) => {
    const [isStarred, setIsStarred] = useState(false);
    const [loggedIn, setLoggedIn, savedProjects, setSavedProjects] = useContext(LoginContext);

    useEffect(() => {
        savedProjects.find(proj => JSON.stringify(proj) === JSON.stringify(props)) !== undefined && setIsStarred(true);
    }, [props, savedProjects, setIsStarred])

    const handleStarClick = (projectID) => {
        loggedIn === '' ? toast.error('Please log in to save a project.', {
            position: 'top-right',
            style: { fontSize: '0.8rem' },
            autoClose: 1000,
            hideProgressBar: true,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            icon: <AiOutlineCloseCircle className="toast-error-icon" />
        }) : (
            handler(projectID)
        );
    };

    const handler = (projectID) => {
        if (isStarred) {
            // This code will allow users to delete saved projects. However, since deleting projects does not actually send a POST, we do not get our desired updates in the backend.
            // This means that after removing a project from a user's saved list, it becomes impossible to add it back.
            // const updatedProjects = savedProjects.filter(proj => JSON.stringify(proj) !== JSON.stringify(props))
            // setSavedProjects(updatedProjects)
            setIsStarred(!isStarred);
            toast.success('Project unsaved!', {
                position: 'top-right',
                style: { fontSize: '0.8rem' },
                autoClose: 1000,
                hideProgressBar: true,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                icon: <AiOutlineCloseCircle />
            });
        } else {
            setIsStarred(!isStarred);
            fetch('/save-project', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: loggedIn,
                    pUID: projectID
                })
            }).then(res => {
                if (res.status === 403) {
                    toast.success('Project already saved!', {
                        position: 'top-right',
                        style: { fontSize: '0.8rem' },
                        autoClose: 1000,
                        hideProgressBar: true,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        icon: <AiOutlineCloseCircle />
                    });
                }
                else if (res.status === 200) {
                    setSavedProjects(prev => [...prev, props])
                    toast.success('Project saved!', {
                        position: 'top-right',
                        style: { fontSize: '0.8rem' },
                        autoClose: 1000,
                        hideProgressBar: true,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                    });
                }
                else {
                    toast.error('Error occurred while saving project!', {
                        position: 'top-right',
                        style: { fontSize: '0.8rem' },
                        autoClose: 1000,
                        hideProgressBar: true,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        icon: <AiOutlineCloseCircle className="toast-error-icon" />
                    });
                }
            });
        }
    };


    return (
        <>
            <ToastContainer toastClassName="toast-no-shadow" />
            <Card bg='light' style={{ width: '100%' }}>
                <Card.Body>
                    <div style={{ paddingBottom: '20px' }}>
                        <Card.Title>
                            <a href={props.gh_rep_url} style={{ color: '#212529', textDecoration: 'none' }}>
                                {props.gh_repo_name}&nbsp;<AiOutlineGithub />
                            </a>
                            <div className='float-end'>
                                <div style={{ cursor: 'pointer', marginRight: '5px' }}>
                                    <AiFillStar
                                        onClick={() => handleStarClick(props.pUID)}
                                        style={{
                                            color: isStarred ? 'gold' : 'grey',
                                            fontSize: '1.5rem'
                                        }}
                                    />
                                </div>
                            </div>
                        </Card.Title>
                        <Card.Subtitle className='mb-1 small' style={{ color: '#007BFF' }}>
                            {props.gh_username}
                            &nbsp;{props.gh_contributing_url !== '' && (
                                <a href={props.gh_contributing_url}
                                    style={{ fontSize: '0.8rem', position: 'relative', color: 'grey' }}>
                                    w/ CONTRIBUTING.md
                                </a>
                            )}
                        </Card.Subtitle>
                        <Card.Subtitle className='mb-2 text-muted small'>
                            <AiOutlineEye /> {props.num_watchers}&nbsp;
                            <AiOutlineFork /> {props.num_forks}&nbsp;
                            <AiOutlineStar /> {props.num_stars}
                        </Card.Subtitle>
                        <Card.Text className='small'>{props.gh_description}</Card.Text>
                    </div>
                    {[1, 2, 3, 4, 5].some(index => props[`gh_topics_${index}`] !== "") && (
                        <div style={{ paddingBottom: '10px' }}>
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
                                            action
                                            style={{
                                                height: 'fit-content',
                                                width: 'fit-content',
                                                borderRadius: '50px',
                                                backgroundColor: '#007BFF',
                                                fontWeight: 'bold',
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
                    )}
                    {[1, 2, 3, 4, 5, 6, 7].some(index => props[`issue_label_${index}`] !== "") && (
                        <div style={{ paddingBottom: '10px' }}>
                            <Card.Subtitle className='mb-1 text-muted small' style={{ background: 'transparent', border: 'none' }}>Issue Labels:</Card.Subtitle>
                            <ListGroup horizontal
                                style={{
                                    display: 'flex',
                                    flexWrap: 'wrap',
                                    listStyle: 'none',
                                    fontSize: '0.5rem',
                                    padding: '0',
                                    margin: '0',
                                }}>
                                {[1, 2, 3, 4, 5, 6, 7].map(index => (
                                    props[`issue_label_${index}`] !== "" && (
                                        <ListGroup.Item
                                            key={index}
                                            action
                                            style={{
                                                height: 'fit-content',
                                                width: 'fit-content',
                                                borderRadius: '50px',
                                                color: '#ffffff',
                                                fontWeight: 'bold',
                                                padding: '5px 10px',
                                                margin: '5px',
                                                backgroundColor: '#555555'
                                            }}>
                                            {props[`issue_label_${index}`]}
                                        </ListGroup.Item>
                                    )
                                ))}
                            </ListGroup>
                        </div>
                    )}
                </Card.Body>
                <Card.Footer>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <small className='text-muted' style={{ fontSize: '0.4rem', padding: '0' }}>Last commit: {props.date_last_commit}</small>
                        <small className='text-muted' style={{ fontSize: '0.4rem', padding: '0' }}>Last merged PR: {props.date_last_merged_PR}</small>
                    </div>
                    <div>
                        <Card.Text className="small" style={{ fontSize: '0.6rem', fontWeight: 'bold' }}>
                            Pigeonhole New Contributor Score&nbsp;
                            <AiOutlineCopyright />
                            :&nbsp;
                            <span style={{ color: props.new_contrib_score > 75 ? '#99C140' : props.new_contrib_score > 45 ? '#E8B100' : '#CC3232', fontSize: '1rem', textShadow: '0.2px 0.2px 0.2px #000000' }}>
                                {props.new_contrib_score}
                            </span>
                            /100
                        </Card.Text>
                    </div>
                </Card.Footer>
            </Card>
        </>
    );
}

export default Project;
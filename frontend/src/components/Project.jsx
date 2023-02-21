/* eslint-disable jsx-a11y/anchor-has-content */

import Card from 'react-bootstrap/Card';
import { AiOutlineStar, AiOutlineFork, AiOutlineEye } from 'react-icons/ai'

const Project = (props) => {
    return (
        <Card bg='light'>
            <Card.Body>
                <Card.Title>{props.gh_repo_name}</Card.Title>
                <Card.Subtitle className='mb-2 text-muted'><AiOutlineEye /> {props.num_watchers}&emsp;<AiOutlineFork /> {props.num_forks}&emsp;<AiOutlineStar /> {props.num_stars}</Card.Subtitle>
                <Card.Text>{props.gh_description}</Card.Text>
                <a href={props.gh_rep_url} class="stretched-link"></a>
            </Card.Body>
            <Card.Footer>
                <small className='text-muted'>Last commit: {props.date_last_commit}</small>
            </Card.Footer>
        </Card>
    );
}

export default Project;
import Card from 'react-bootstrap/Card';

const Project = (props) => {
    return (
        <Card>
            <Card.Title>{props.gh_repo_name}</Card.Title>
        </Card>
    );
}

export default Project;
import { Container } from "react-bootstrap";

const NotFound = () => {
    return (
        <>
            <Container className="mt-3">
                <h1>404.</h1>
                <p>could not find resource</p>
            </Container>
        </>
    );
};

export default NotFound;
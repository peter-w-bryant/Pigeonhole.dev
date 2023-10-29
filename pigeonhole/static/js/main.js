function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling animation
    });
}

window.addEventListener('scroll', () => {
    const button = document.getElementById('back-to-top-button');
    if (window.scrollY > 200) {
        button.style.display = 'block'; // Show the button when scroll position is greater than 200px
    } else {
        button.style.display = 'none'; // Hide the button when scroll position is less than 200px
    }
});

window.addEventListener('load', () => {

    // JavaScript to handle form submission and AJAX request on any change to the search input
    document.getElementById('search-form').addEventListener('submit', (e) => {
        console.log('Form submitted');
        e.preventDefault();
        const searchQuery = document.getElementById('search-input').value;

        // Make an AJAX request to Flask
        fetch('/api/search', {
            method: 'POST',
            body: JSON.stringify({ query: searchQuery }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                // Replace everything in  <div class="project-container"> with a project square
                // for each project in the response
                const projectContainer = document.querySelector('.project-container');
                projectContainer.innerHTML = '';

            });
    });

});
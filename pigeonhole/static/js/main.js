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

    // JavaScript to handle form submission and AJAX request
    document.getElementById('search-form').addEventListener('submit', function (e) {
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
                // Update the project list with the filtered data
                const projectList = document.getElementById('project-list');
                console.log(data);
                // Update the project list with the filtered data
                // You can use data to update the project list
            });
    });

});
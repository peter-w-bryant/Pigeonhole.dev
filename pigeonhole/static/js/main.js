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

    // JavaScript to handle form submission and filtering projects from projects.json
    document.getElementById('search-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const searchQuery = document.getElementById('search-input').value;
        const projectContainer = document.getElementById('project-container');
        projectContainer.innerHTML = '';
        // Read in static_data/projects.json
        fetch('api/static_data/projects.json')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                console.log(data)
                // Data is a json object mapping github url to project dict
                // for key value pairs in data
                for (const [key, value] of Object.entries(data)) {
                    // If the project name contains the search query
                    if (value.repo_name.toLowerCase().includes(searchQuery.toLowerCase())) {
                        // Create a new project card
                        const projectCard = document.createElement('div');
                        projectCard.className = 'project-card';
                        projectCard.innerHTML = `
                            <div class="project-card-text">
                                <h3>${value.repo_name}</h3>
                                <p>${value.gh_description}</p>
                            </div>
                        `;
                        // Add the project card to the project container
                        projectContainer.appendChild(projectCard);
                    }
                }
            });
    });

});
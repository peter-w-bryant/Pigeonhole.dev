// Add event listener to scroll and back-to-top button
window.addEventListener('scroll', displayScrollBtn);
document.getElementById('back-to-top-button').addEventListener('click', scrollToTop);

function displayScrollBtn() {
    const button = document.getElementById('back-to-top-button');
    if (window.scrollY > 200) {
        button.style.display = 'block'; // Show the button when scroll position is greater than 200px
    } else {
        button.style.display = 'none'; // Hide the button when scroll position is less than 200px
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling animation
    });
}
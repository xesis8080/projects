// Get the search input element
const searchBar = document.getElementById('search-bar');

// Get all genre cards
const genreCards = document.querySelectorAll('.card');

// Add an event listener to the search input
searchBar.addEventListener('input', function () {
    const searchTerm = searchBar.value.toLowerCase();

    // Loop through each genre card and check if it matches the search query
    genreCards.forEach(card => {
        const cardHeading = card.querySelector('h2').textContent.toLowerCase();
        if (cardHeading.includes(searchTerm)) {
            card.style.display = 'block'; // Display matching cards
        } else {
            card.style.display = 'none'; // Hide non-matching cards
        }
    });
});

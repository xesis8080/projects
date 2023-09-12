// Function to fetch card data from Flask and add cards to the section
function fetchAndAddCards() {
    // Make an AJAX request to your Flask endpoint to get card data
    fetch('/get_card_data')
        .then(response => response.json())
        .then(data => {
            // Loop through the data and create a card for each item
            data.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('card', 'genre-card'); // Add a class to identify the cards

                const cardHeading = document.createElement('h2');
                cardHeading.textContent = item.heading;

                // Add event listener to the "View More" button if needed

                const cardImg = document.createElement('img');
                cardImg.src = item.imgSrc;
                cardImg.alt = item.heading;

                const viewMoreButton = document.createElement('button');
                viewMoreButton.textContent = 'List Books';

                card.appendChild(cardHeading);
                card.appendChild(cardImg);
                card.appendChild(viewMoreButton);

                document.getElementById('card-section').appendChild(card);
                viewMoreButton.addEventListener('click', function () {
                    window.location.href = `/genre_books?genre=${item.heading}`;
                });
            });
            
            // Call the function to enable search functionality
            enableSearch(data.map(item => item.heading.toLowerCase().replace(/\s/g, ''))); // Remove spaces from headings
        })
        .catch(error => {
            console.error('Error fetching card data:', error);
        });

}

// Function to enable the search functionality and filter the cards
function enableSearch(headings) {
    const searchBar = document.getElementById('search-bar');
    const genreCards = document.querySelectorAll('.genre-card');

    searchBar.addEventListener('input', function () {
        const searchTerm = searchBar.value.toLowerCase().replace(/\s/g, ''); // Remove spaces from the search term

        genreCards.forEach((card, index) => {
            const cardHeading = headings[index]; // Get the preprocessed heading
            if (cardHeading.includes(searchTerm)) {
                card.style.display = 'flex'; // Display matching cards
            } else {
                card.style.display = 'none'; // Hide non-matching cards
            }
        });
    });
}

// Call the function to fetch and add cards when the page loads
window.addEventListener('load', fetchAndAddCards);

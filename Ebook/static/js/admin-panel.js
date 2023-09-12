 // CODE FOR DYNAMIC BOOKS LOADING #########
 function populateBooks(selectedGenre) {
    const bookSelect = document.getElementById('book');
    // Clear existing options
    bookSelect.innerHTML = '';

    // Make an AJAX request to fetch books based on the selected genre
    fetch('/get_books_by_genre?genre=' + selectedGenre)
        .then(response => response.json())
        .then(data => {
            // Populate the books <select> with the received data
            data.forEach(book => {
                const option = document.createElement('option');
                option.value = book.id; // Use a unique identifier for each book
                option.textContent = book.title; // Display the book title
                bookSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
}


document.addEventListener('DOMContentLoaded', function () {
    const genreSelect = document.getElementById('genre1');
    
    // Fetch genre headings using a GET request to your server
    fetch('/get_genres', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Populate the dropdown options
        data.genres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre.id;
            option.textContent = genre.heading;
            genreSelect.appendChild(option);
        });
    
    })
    .catch(error => {
        console.error('Error fetching genres:', error);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const genreSelect = document.getElementById('genre2');
    
    // Fetch genre headings using a GET request to your server
    fetch('/get_genres', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Populate the dropdown options
        data.genres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre.id;
            option.textContent = genre.heading;
            genreSelect.appendChild(option);
        });
    
    })
    .catch(error => {
        console.error('Error fetching genres:', error);
    });
});


// ADD REMOVE BOOKS 
document.addEventListener('DOMContentLoaded' , function() {
    const genreSelect = document.getElementById('genre3');
    const bookSelect = document.getElementById('book');
    // Fetch genre headings using a GET request to your server
    fetch('/get_genres', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Populate the dropdown options
        data.genres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre.id;
            option.textContent = genre.heading;
            genreSelect.appendChild(option);
        });

         // Add an event listener to update book options when the genre selection changes
         genreSelect.addEventListener('change', function () {
            const selectedGenre = this.value;
            populateBooks(selectedGenre);
        });

        // Automatically load books for the first genre (if available)
        if (data.genres.length > 0) {
            const firstGenreId = data.genres[0].id;
            populateBooks(firstGenreId);
        }
    
    })
    .catch(error => {
        console.error('Error fetching genres:', error);
    });
    const removeBookButton = document.getElementById('remove-book-button');

    // Event listener for the "Remove Book" button
    removeBookButton.addEventListener('click', function () {
        const selectedGenre = genreSelect.value;
        const selectedBook = bookSelect.value;

        if (selectedGenre && selectedBook) {
            // Make an AJAX request to remove the book from the selected genre
            fetch('/remove_book_from_genre', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    genreId: selectedGenre,
                    bookId: selectedBook
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Book removed from genre.');
                    window.location.reload();
                    // You can update the UI or take other actions as needed.
                } else {
                    alert('Failed to remove the book from the genre.'+data.message);
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error removing book from genre:', error);
            });
        } else {
            alert('Please select both a genre and a book to remove.');
        }
    });
});

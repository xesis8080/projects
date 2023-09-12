from app import *
import os
from sqlalchemy.exc import PendingRollbackError , IntegrityError # Import the exception
from PIL import Image

# BASIC ROUTES
@app.route('/')
def redirection():
    return redirect('/authentication')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/admin-panel')
def admin_panel():
    return render_template('admin-panel.html')

from urllib.parse import quote

@app.template_filter('url_encode')
def url_encode_filter(s):
    return quote(s)


##########################################################
# Replace this with your database logic to fetch card data
def get_card_data():
    card_data = []

    # Fetch genre data from the database
    genres = Genre.query.all()

    # Convert the genre objects to a format suitable for your cards
    for genre in genres:
        card_data.append({
            'heading': genre.heading,
            'imgSrc': f"/static/images/{genre.image}",  # Assuming you store the image path in the 'image' field
        })

    return card_data

@app.route('/get_card_data')
def get_cards():
    card_data = get_card_data()
    return jsonify(card_data)

###### ADD A GENRE CODE #########################################

# Set the path for storing uploaded images relative to the 'static' folder
UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to handle genre uploads
@app.route('/upload_genre', methods=['POST'])
def upload_genre():
    heading = request.form.get('heading')
    image = request.files['image']

    if not heading:
        return jsonify({'success': False, 'message': 'Heading is required'})

    if not image:
        return jsonify({'success': False, 'message': 'Image is required'})
    
    existing_genre = Genre.query.filter_by(heading=heading).first()
    if existing_genre:
        return jsonify({'success': False, 'message': 'Genre heading is already in Use . Change it and try again'})
    existing_image = Genre.query.filter_by(image=image.filename).first()
    if existing_image:
        return jsonify({'success': False, 'message': 'Image with this name already exists . Please Change Name and try again'})

    desired_aspect_ratio = (4, 3)

    # ...

    try:
            # Open the uploaded image using Pillow
            img = Image.open(image)
            img = img.convert('RGB')
            # Calculate the desired width based on the aspect ratio
            desired_width = int(img.height * (desired_aspect_ratio[0] / desired_aspect_ratio[1]))

            # Resize and crop the image to the desired aspect ratio
            img = img.resize((desired_width, img.height), Image.ANTIALIAS)
            left_margin = (img.width - desired_width) // 2
            right_margin = img.width - left_margin
            img = img.crop((left_margin, 0, right_margin, img.height))

            # Save the cropped image with a unique filename
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            img.save(image_filename)
            genre = Genre(heading=heading, image=image.filename , genre_id=heading)
            db.session.add(genre)
            db.session.commit()

                # Respond with a success message and the image path
            return jsonify({'success': True, 'message': 'Genre uploaded successfully', 'image_path': image_filename})
    except Exception as e:
            return jsonify({'success': False, 'message': f'Upload Failed : {str(e)}'})
    
############# Remove genre #####################
@app.route('/get_genres', methods=['GET'])
def get_genres():
    # Fetch genre data from the database
    genres = Genre.query.all()
    genre_list = [{'id': genre.id, 'heading': genre.heading} for genre in genres]
    return jsonify({'genres': genre_list})

@app.route('/remove_genre', methods=['POST'])
def remove_genre_post():
    genre_id = request.form.get('genre')
    
    if genre_id:
        # Retrieve the genre from the database based on its ID
        genre = Genre.query.get(int(genre_id))
        
        if genre:
            # Get the associated image file path
            image_file_path = genre.image

            # Delete the associated books from the database
            associated_books = Book.query.filter_by(genre_id=genre.id).all()
            for book in associated_books:
                db.session.delete(book)
            
            # Delete the genre from the database
            db.session.delete(genre)
            db.session.commit()

            # Check if the image file exists and delete it
            if image_file_path and os.path.exists(image_file_path):
                os.remove(image_file_path)
    
    return jsonify({'success': True})

############ Remove the book#########################

@app.route('/remove_book_from_genre', methods=['POST'])
def remove_book_from_genre():
    data = request.json
    genre_id = data.get('genreId')
    book_id = data.get('bookId')

    if genre_id and book_id:
        try:
            # Remove the association between the book and genre
            association = BookGenre.query.filter_by(genre_id=genre_id, book_id=book_id).first()
            if association:
                db.session.delete(association)

                # Delete the book itself from the database
                book = Book.query.get(book_id)
                if book:
                    db.session.delete(book)

                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Book not found in the genre.'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    return jsonify({'success': False})


############ Define a route to handle book uploads #############################

@app.route('/upload_book', methods=['POST'])
def upload_book():
    try:
        # Get form data
        book_title = request.form['book-title']
        author = request.form['author']
        genre_id = request.form['genre']  # Assuming you have a genre ID here

        # Handle the file upload
        uploaded_file = request.files['book-file']
        if uploaded_file:
            # Save the file to the "ebooks" subdirectory in the static folder
            static_folder=os.path.join(app.static_folder,'ebooks')
            os.makedirs(static_folder,exist_ok=True)
            file_path = os.path.join(static_folder, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Create a new Book entry in the database
            new_book = Book(title=book_title, author=author, genre_id=genre_id, file_path=file_path)
            db.session.add(new_book)
            db.session.commit()
            try:
                # Check if the association already exists
                association = BookGenre.query.filter_by(genre_id=genre_id, book_id=new_book.id).first()
                if not association:
                    # Create a new association between the book and genre
                    association = BookGenre(genre_id=genre_id, book_id=new_book.id)
                    db.session.add(association)
                    db.session.commit()
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, 'message': 'Book already exists in the genre.'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})

        else:
            return jsonify(success=False, message='No file selected.')
    except Exception as e:
        return jsonify(success=False, message=str(e))
    
################# ADD OR REMOVE BOOKS #########################
# Define a route to fetch books by genre
@app.route('/get_books_by_genre')
def get_books_by_genre():
    selected_genre = request.args.get('genre')  # Get the selected genre from the request

    # Query the database to fetch books for the selected genre
    books = Book.query.filter_by(genre_id=selected_genre).all()

    # Create a list of book data
    book_data = [{'id': book.id, 'title': book.title} for book in books]

    return jsonify(book_data)

################# LIIST BOOKS ##################################
@app.route('/genre_books', methods=['GET'])
def genre_books():
    genre_heading = request.args.get('genre')

    # Query the database to fetch the genre based on the heading
    genre = Genre.query.filter_by(heading=genre_heading).first()

    if genre:
        # Fetch books associated with the genre
        books = Book.query.filter_by(genre_id=genre.id).all()
        return render_template('genre_books.html', genre_heading=genre_heading, books=books)
    else:
        # Handle the case where the genre is not found
        return render_template('genre_books.html', genre_heading=genre_heading, books=None)

@app.route('/download_book/<path:filename>')
def download_book(filename):
    # Define the directory where your book files are stored
    static_folder = os.path.join(app.static_folder, 'ebooks')
    file_path = os.path.join(static_folder, filename)

    if os.path.exists(file_path):
        try:
            # Open the file and serve it as an attachment
           with open(file_path, 'rb') as file:
                response = Response(file.read())
                response.headers['Content-Type'] = 'application/pdf'  # Set the Content-Type as needed
                response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                return response
        except Exception as e:
            # Handle any exceptions that may occur during file reading
            return f"Error: {str(e)}", 500  # Internal Server Error
    else:
        # Return a 404 error if the file does not exist
        return 404

if __name__ == '__main__':
    app.run(debug=True)


################# Before and after request authentication checks #####################################
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.before_request
def before_specific_route():
    if request.path == '/':
        if 'user_id' in session:
            return redirect('/home')
    elif request.path == '/authentication':
        if 'user_id' in session:
            return redirect('/home')
    elif request.path == '/admin-panel':
        if ('user_id' in session) & (session['role']=="Admin"):
            return render_template("admin-panel.html")
        else:
            return redirect('/home')

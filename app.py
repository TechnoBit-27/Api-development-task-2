from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_DIR = 'data'
BOOKS_FILE = os.path.join(DATA_DIR, 'books.json')
STUDENT_FILE = os.path.join(DATA_DIR, 'students.json')


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    books = load_data(BOOKS_FILE)
    return jsonify(books)

@app.route('/add_book', methods=['POST'])
def add_book():
    book = request.json
    books = load_data(BOOKS_FILE)
    books.append({**book, 'status': 'available'})
    save_data(BOOKS_FILE, books)
    return '', 200

@app.route('/remove_book', methods=['POST'])
def remove_book():
    book_data = request.json
    book_id = book_data['id']
    books = load_data(BOOKS_FILE)
    books = [book for book in books if book['id'] != book_id]
    save_data(BOOKS_FILE, books)
    return '', 200

@app.route('/return_book', methods=['POST'])
def return_book():
    book_data = request.json
    book_id = book_data['id']
    books = load_data(BOOKS_FILE)
    for book in books:
        if book['id'] == book_id and book['status'] == 'issued':
            book['status'] = 'available'
            book.pop('issued_to', None)
            save_data(BOOKS_FILE, books)
            return '', 200
    return 'Book not found or not issued', 400

if __name__ == '__main__':
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    app.run(debug=True)

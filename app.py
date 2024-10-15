from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flashcard_db"
mongo = PyMongo(app)

#while adding try/catch is good, i don't know why it doesn't work if i removed them


@app.route('/')
def index():
    try:
        flashcard = list(mongo.db.flashcards.aggregate([{'$sample': {'size': 1}}]))  # Get a random flashcard
        if flashcard:
            flashcard = flashcard[0]
        else:
            flashcard = None
        return render_template('index.html', flashcard=flashcard)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"

@app.route('/modify')
def modify():
    try:
        flashcards = mongo.db.flashcards.find().sort("figure_of_speech")
        return render_template('modify.html', flashcards=flashcards)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"


@app.route('/find_word', methods=['POST'])
def find_word():
    try:
        word = request.form.get('word')
        flashcard = mongo.db.flashcards.find_one({'word': word})
        result = mongo.db.flashcards.delete_one({'word': word})
        if result:
            if result.deleted_count:
                return render_template('modify.html', flashcards=mongo.db.flashcards.find(), message=f"Flashcard '{word}' deleted")
            else:
                return render_template('modify.html', flashcards=mongo.db.flashcards.find(), warning="Word not in database")
        else:
            return render_template('modify.html', flashcards=mongo.db.flashcards.find(), warning="Word not found")
    except Exception as e:
        app.logger.error(f"Error finding flashcard: {e}")
        return f"Error finding flashcard: {e}"


@app.route('/test')
def test():
    try:
        flashcards = mongo.db.flashcards.find()
        return render_template('test.html', flashcards=flashcards)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"

@app.route('/add', methods=['POST'])
def add_flashcard():
    try:
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        figure_of_speech = request.form.get('figure_of_speech')
        print(f"Received data - Word: {word}, Meaning: {meaning}, Figure of Speech: {figure_of_speech}")
        if word and meaning and figure_of_speech:
            mongo.db.flashcards.insert_one({
                'word': word,
                'meaning': meaning,
                'figure_of_speech': figure_of_speech
            })
            print("Flashcard added to the database")
        else:
            print("Missing data, flashcard not added")
        return redirect(url_for('modify'))
    except Exception as e:
        app.logger.error(f"Error adding flashcard: {e}")
        return f"Error adding flashcard: {e}"

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    try:
        flashcards = list(mongo.db.flashcards.find())
        return jsonify(flashcards)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"

@app.route('/flashcard/<word>', methods=['POST'])
def delete_flashcard(word):
    try:
        if request.form.get('_method') == 'DELETE':
            result = mongo.db.flashcards.delete_one({'word': word})
            if result.deleted_count:
                print(f"Flashcard '{word}' deleted")
                return redirect(url_for('modify'))
            else:
                print(f"Flashcard '{word}' not found")
                return jsonify({'error': 'Flashcard not found'}), 404
        return jsonify({'error': 'Invalid method'}), 405
    except Exception as e:
        app.logger.error(f"Error deleting flashcard: {e}")
        return f"Error deleting flashcard: {e}"

@app.route('/check_db')
def check_db():
    try:
        # Attempt to fetch a document from the collection
        mongo.db.flashcards.find_one()
        return "Database connection successful!"
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return f"Database connection failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)


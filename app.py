from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
import random

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flashcard_db"
mongo = PyMongo(app)

#while adding try/catch is good, i don't know why it doesn't work if i removed them


@app.route('/')
def index():
    try:
        flashcard = list(mongo.db.flashcards.aggregate([{'$sample': {'size': 1}}]))  #  random flashcard
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
        sort_by = request.args.get('sort_by', 'word')  #  sort by word
        sort_order = request.args.get('sort_order', 'asc')  #sort order ascending
        sort_order = 1 if sort_order == 'asc' else -1
        page = int(request.args.get('page', 1))
        per_page = 25

        flashcards = mongo.db.flashcards.find().sort(sort_by, sort_order).skip((page - 1) * per_page).limit(per_page)
        total_flashcards = mongo.db.flashcards.count_documents({})
        total_pages = (total_flashcards + per_page - 1) // per_page

        return render_template('modify.html', flashcards=flashcards, sort_by=sort_by, sort_order=sort_order, page=page, total_pages=total_pages)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"


@app.route('/findel_word', methods=['POST'])
def findel_word():
    try:
        word = request.form.get('word')
        #flashcard = mongo.db.flashcards.find_one({'word': word})
        result = mongo.db.flashcards.delete_one({'word': word})
        
        # page is undefined ...?
 

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

@app.route('/find', methods=['POST'])
def find():
    try:
        word = request.args.get('word')
        flashcard = mongo.db.flashcards.find_one({'word': word})
        if flashcard:
            return jsonify({'word': flashcard['word'], 'meaning': flashcard['meaning'], 'figure_of_speech': flashcard['figure_of_speech']})
        else:
            return jsonify({'error': 'Word not found'})
    except Exception as e:
        app.logger.error(f"Error finding flashcard: {e}")
        return jsonify({'error': f"Error finding flashcard: {e}"})
    

@app.route('/quiz')
def quiz():
    try:
        flashcards = list(mongo.db.flashcards.aggregate([{'$sample': {'size': 5}}]))  # get 5 random and quiz them
        all_flashcards = list(mongo.db.flashcards.find({}))
        for flashcard in flashcards:
            incorrect_options = random.sample([fc['meaning'] for fc in all_flashcards if fc['word'] != flashcard['word']], 3)
            flashcard['options'] = incorrect_options + [flashcard['meaning']]
            random.shuffle(flashcard['options'])
        return render_template('quiz.html', flashcards=flashcards)
    except Exception as e:
        app.logger.error(f"Error fetching flashcards: {e}")
        return f"Error fetching flashcards: {e}"

@app.route('/check_answers', methods=['POST'])
def check_answers():
    try:
        results = []
        for i in range(1, 6):
            word = request.form.get(f'word_{i}')
            user_meaning = request.form.get(f'meaning_{word}')
            flashcard = mongo.db.flashcards.find_one({'word': word})
            correct_meaning = flashcard['meaning'] if flashcard else None
            results.append({
                'word': word,
                'user_meaning': user_meaning,
                'correct_meaning': correct_meaning,
                'is_correct': user_meaning == correct_meaning if correct_meaning else False
            })
        return render_template('results.html', results=results)
    except Exception as e:
        app.logger.error(f"Error checking answers: {e}")
        return f"Error checking answers: {e}"

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
        #  to fetch a document from the collection
        mongo.db.flashcards.find_one()
        return "Database connection successful!"
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return f"Database connection failed: {e}"




if __name__ == '__main__':
    app.run(debug=True)


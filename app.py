from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flashcard_db"
mongo = PyMongo(app)


@app.route('/')
def index():
    flashcards = mongo.db.flashcards.find()
    return render_template('index.html', flashcards=flashcards)

@app.route('/modify')
def modify():
    flashcards = mongo.db.flashcards.find().sort("figure of speech")
    return render_template('modify.html', flashcards=flashcards)

@app.route('/test')
def test():
    flashcards = mongo.db.flashcards.find()
    return render_template('test.html', flashcards=flashcards)


@app.route('/add', methods=['POST'])
def add_flashcard():
    word = request.form.get('word')
    meaning = request.form.get('meaning')
    figure = request.form.get('figure')
    if word and meaning and figure:
        mongo.db.flashcards.insert_one({'word': word, 'meaning': meaning, "figure of speech": figure })
    return redirect(url_for('index'))


@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = list(mongo.db.flashcards.find())
    return jsonify(flashcards)


@app.route('/flashcard/<word>', methods=['GET'])
def get_flashcard(word):
    flashcard = mongo.db.flashcards.find_one({'word': word})
    if flashcard:
        return jsonify(flashcard)
    return jsonify({'error': 'Flashcard not found'}), 404


@app.route('/flashcard/<word>', methods=['DELETE'])
def delete_flashcard(word):
    result = mongo.db.flashcards.delete_one({'word': word})
    if result.deleted_count:
        return jsonify({'message': 'Flashcard deleted'})
    return jsonify({'error': 'Flashcard not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)


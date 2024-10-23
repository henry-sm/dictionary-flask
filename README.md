# Vocabulary Flashcards

Made for ADBMS mini-project to showcase CRUD applicaitons.
A applcation made to improve one's vocabulary with the help of flashcards which are created and maintained by the user based on the words they choose to learn. This also contains a quiz which tests the user for a particular word

## Techbologies used 
- Flask
- MonogoDB

## Features

- Add, view, update, and delete flashcards.
-  Generate quizz based on flashcards.
- Search for specific words in the database and view their meanings.

## Pages 

- **Home Page**: View a random flashcard.
- **Modify Page**: Add, update, and delete flashcards.
- **Quiz Page**: Take quizzes to test your vocabulary knowledge.
- **Search**: Find specific words and their meanings.


## Setting up 

1. **Clone the repository**:
    ```bash
    git clone https://github.com/henry-sm/dictionary-flask.git
    cd dictionary-flask
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    venv\\Scripts\\activate.bat
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB**:
    - Connect `app.py` with Mongodb
      ```python
      app.config["MONGO_URI"] = "mongodb://localhost:27017/flashcard_db"
      ```

5. **Run the application**:
    ```bash
    python app.py
    ```
    Application should be up and running at `http://127.0.0.1:5000/` 

🐍 Python Assignment #3 – Enhanced Hangman Game 🎮
📝 Description
This project is an enhancement of the classic Hangman game (hangman.py) implemented in Python. The assignment focuses on improving the user experience through:

Difficulty levels

Expanded word sets

Interactive menus

Player statistics tracking using SQLite

✅ Features Implemented
🔹 1. Levels of Difficulty
The game now supports three levels of gameplay:


Level	Word Set Choice	Number of Trials	Hints
Easy	User chooses from Animals, Shapes, or Places	8	Set is revealed
Moderate	User chooses from Animals, Shapes, or Places	6	Set is revealed
Hard	Set and word both randomly selected	6	No hints
🔹 2. Word Sets Added
The original game only supported Animals. We've added two more:

Shapes: square, triangle, rectangle, circle, ellipse, rhombus, trapezoid

Places: Cairo, London, Paris, Baghdad, Istanbul, Riyadh

🔹 3. Hall of Fame (Score Tracking)
A local SQLite database is used to store high scores for each level.

Database Fields:

Player Name

Level

Remaining Lives

Example Table:


Level	Winner Name	Remaining Lives
Easy	John	6
Moderate	Nancy	5
Hard	Ahmed	3
🔹 4. Menus and User Interface
Using a clean and structured menu interface built with TableT (or any tabular print library):

👤 Welcome Screen: Asks for player name

📋 Main Menu:

Play the Game (Choose difficulty)

Hall of Fame

About the Game

📚 About Menu: Provides game instructions and rules

Menus are re-displayed after game completion for smooth replayability.

⚙️ How to Run
bash
Copy
Edit
python 1_Question.py
Make sure sqlite3 and any external libraries (e.g., tableprint or tabulate) are installed if used:

bash
Copy
Edit
pip install tabulate
🧠 About the Game
text
Copy
Edit
Easy: Choose the set (Animals/Shapes/Places), 8 lives
Moderate: Choose the set, 6 lives
Hard: Random set & word, 6 lives, no clue

Guess the letters of the hidden word before you run out of lives!
🏁 Evaluation Criteria
✔️ Functionality
Fully working game with menus and database integration

Error handling for invalid inputs

Reusable code with proper functions and structures

✔️ Code Quality
Clear and consistent naming conventions

Modularized functions, no repetition

Proper commenting, formatting, and indentation

✔️ User Experience
Friendly CLI with well-formatted menus

Hall of Fame leaderboard

Replayability and easy-to-follow instructions

📦 File Structure
bash
Copy
Edit
3_Question.py         # Main game script
3_Question.db         # SQLite database (created automatically)
README.md          # Project documentation (this file)
🙌 Credits
Developed by: Vineet Vardhan
Python Assignment 

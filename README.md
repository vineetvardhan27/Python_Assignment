# 🐍 Python Assignment #3 – Enhanced Hangman Game 🎮

## 📝 Description

This project is an enhancement of the classic **Hangman** game (`3_Question.py`) implemented in Python. The goal is to improve the user experience with new levels of difficulty, additional word sets, an interactive menu system, and score tracking using an SQLite database.

---

## ✅ Features Implemented

### 🔹 1. **Levels of Difficulty**

The game now supports **three levels** of gameplay:

| **Level**   | **Word Set Choice**                           | **Number of Trials** | **Hints**         |
|-------------|-----------------------------------------------|----------------------|-------------------|
| Easy        | User chooses from `Animals`, `Shapes`, or `Places` | 8                    | Set is revealed   |
| Moderate    | User chooses from `Animals`, `Shapes`, or `Places` | 6                    | Set is revealed   |
| Hard        | Random set & word                              | 6                    | No hints provided |

---

### 🔹 2. **Word Sets Added**

In addition to the original **Animals** set, the game now includes:

- **Shapes**: square, triangle, rectangle, circle, ellipse, rhombus, trapezoid  
- **Places**: Cairo, London, Paris, Baghdad, Istanbul, Riyadh

---

### 🔹 3. **Hall of Fame (Score Tracking)**

A local **SQLite** database tracks high scores based on remaining lives.

**Database Fields:**
- Player Name
- Level (Easy, Moderate, Hard)
- Remaining Lives

**Example Table:**

| **Level**   | **Winner Name** | **Remaining Lives** |
|-------------|------------------|----------------------|
| Easy        | John             | 6                    |
| Moderate    | Nancy            | 5                    |
| Hard        | Ahmed            | 3                    |

---

### 🔹 4. **Menus and User Interface**

A user-friendly interface built with `TableT` or similar library provides:

- 👤 **Welcome Screen**: Prompts for the player’s name  
- 📋 **Main Menu**:
  - Play the Game (select difficulty)
  - Hall of Fame
  - About the Game
- 📚 **About the Game**: Game instructions and explanation of difficulty levels  
- 🔁 Menu redisplays after each game for smooth replay

---

## ⚙️ How to Run

```bash
python 3_Question.py
```

Make sure `sqlite3` and required libraries (e.g., `tabulate` or `tableprint`) are installed:

```bash
pip install tabulate
```

---

## 🧠 About the Game

```
Easy     : Choose the word set (Animals, Shapes, Places), 8 lives
Moderate : Choose the word set, 6 lives
Hard     : Random set and word, 6 lives, no clue

Goal: Guess the word by suggesting letters before you run out of lives!
```

---

## 🏁 Evaluation Criteria

### ✔️ Functionality
- All game features implemented
- SQLite database tracks high scores
- Robust error handling
- Reusable functions and no repeated code

### ✔️ Code Quality
- Clear naming conventions
- Proper commenting and indentation
- Modular structure and clean logic

### ✔️ User Experience
- Friendly and clear menus
- Easy to navigate
- Hall of Fame leaderboard
- Replay and instruction options

---

## 📦 File Structure

```
3_Question.py       # Main game script
3_Question.db       # SQLite database (auto-created)
README.md           # Project documentation (this file)
```

---

## 🙌 Credits

**Developed by:** Vineet Vardhan  
**Assignment:** Python Assignment 

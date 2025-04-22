import random
import sqlite3

word_sets = {
    "Animals": ["ant", "baboon", "badger", "bat", "bear", "beaver", "camel", "cat", "clam", "cobra"],
    "Shapes": ["square", "triangle", "rectangle", "circle", "ellipse", "rhombus", "trapezoid"],
    "Places": ["cairo", "london", "paris", "baghdad", "istanbul", "riyadh"]
}

# --- Database Functions ---
def create_table():
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            level TEXT PRIMARY KEY,
            winner_name TEXT,
            remaining_lives INTEGER
        )
    ''')
    # Initialize default high scores if the table is newly created
    default_scores = [('Easy', None, -1), ('Moderate', None, -1), ('Hard', None, -1)]
    cursor.executemany('''
        INSERT OR IGNORE INTO high_scores (level, winner_name, remaining_lives)
        VALUES (?, ?, ?)
    ''', default_scores)
    conn.commit()
    conn.close()

def get_high_scores():
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT level, winner_name, remaining_lives FROM high_scores")
    scores = cursor.fetchall()
    conn.close()
    return scores

def update_high_score(level, winner_name, remaining_lives):
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE high_scores
        SET winner_name = ?, remaining_lives = ?
        WHERE level = ? AND remaining_lives < ?
    ''', (winner_name, remaining_lives, level, remaining_lives))
    conn.commit()
    conn.close()

def display_hall_of_fame():
    print("\n" + "=" * 20)
    print("HALL OF FAME")
    print("=" * 20)
    print("{:<10} {:<15} {}".format("Level", "Winner name", "Remaining lives"))
    scores = get_high_scores()
    for level, winner, lives in scores:
        print("{:<10} {:<15} {}".format(level, winner if winner else "-", lives if lives != -1 else "-"))
    print("=" * 20)

# --- Game Logic ---
create_table() # Initialize the database table

print("Welcome to Hangman!")

player_name = input("Enter your name: ").strip()

while True:
    difficulty = input("Choose difficulty (Easy, Moderate, Hard): ").strip().capitalize()
    if difficulty in ["Easy", "Moderate", "Hard"]:
        break
    else:
        print("Invalid choice. Please enter Easy, Moderate, or Hard.")

secret_word = ""
lives = 0
category_hint = ""

if difficulty == "Easy":
    lives = 8
    print("\nDifficulty: Easy (8 lives)")
    while True:
        print("\nAvailable categories:", ", ".join(word_sets.keys()))
        chosen_category = input("Choose a category for the secret word: ").strip().capitalize()
        if chosen_category in word_sets:
            selected_word_list = word_sets[chosen_category]
            secret_word = random.choice(selected_word_list)
            category_hint = f"Hint: The category is {chosen_category}."
            print(f"Okay, the word will be chosen from '{chosen_category}'.")
            break
        else:
            print("Invalid category. Please choose from the list.")

elif difficulty == "Moderate":
    lives = 6
    print(f"\nDifficulty: Moderate ({lives} lives)")
    while True:
        print("\nAvailable categories:", ", ".join(word_sets.keys()))
        chosen_category = input("Choose a category for the secret word: ").strip().capitalize()
        if chosen_category in word_sets:
            selected_word_list = word_sets[chosen_category]
            secret_word = random.choice(selected_word_list)
            category_hint = f"Hint: The category is {chosen_category}."
            print(f"Okay, the word will be chosen from '{chosen_category}'.")
            break
        else:
            print("Invalid category. Please choose from the list.")

elif difficulty == "Hard":
    lives = 6
    print(f"\nDifficulty: Hard ({lives} lives)")
    random_category_name = random.choice(list(word_sets.keys()))
    selected_word_list = word_sets[random_category_name]
    secret_word = random.choice(selected_word_list)
    category_hint = "Hint: No category hint for Hard mode!"
    print("A secret word has been chosen from a random category. Good luck!")

guessed_letters = []
display_word = ["_"] * len(secret_word)
initial_lives = lives

print("\nLet's start guessing!")
if category_hint:
    print(category_hint)

# Assuming 'stages' is defined elsewhere in your full code
# For this example, we'll comment out the graphics part
# if 'stages' in locals():
#     print(stages[lives])

while lives > 0:
    # if 'stages' in locals():
    #     stage_index = lives if difficulty == "Easy" else lives # Adjust if your stages list is different
    #     print(stages[stage_index])

    print(f"\nWord: {' '.join(display_word)}")
    print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
    print(f"Lives remaining: {lives}")

    guess = input("Guess a letter: ").lower().strip()

    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input. Please enter a single letter.")
        continue
    if guess in guessed_letters:
        print(f"You already guessed '{guess}'. Try again.")
        continue

    guessed_letters.append(guess)

    if guess in secret_word:
        print(f"Good guess! '{guess}' is in the word.")
        for i in range(len(secret_word)):
            if secret_word[i] == guess:
                display_word[i] = guess
    else:
        print(f"Sorry, '{guess}' is not in the word.")
        lives -= 1

    if "_" not in display_word:
        print("\n-----------------------------------")
        # if 'stages' in locals(): print(stages[lives])
        print(f"Word: {' '.join(display_word)}")
        print(f"\nCongratulations, {player_name}! You guessed the word: '{secret_word}'")
        print("-----------------------------------")
        update_high_score(difficulty, player_name, initial_lives - (initial_lives - lives)) # remaining lives at win
        break

if lives == 0:
    print("\n-----------------------------------")
    # if 'stages' in locals(): print(stages[0])
    print("\nGame Over! You ran out of lives.")
    print(f"The secret word was: '{secret_word}'")
    print("-----------------------------------")

display_hall_of_fame()
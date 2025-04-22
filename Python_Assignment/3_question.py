import random
import sqlite3
from texttable import Texttable

# Let's define our word sets, nice and organized in a dictionary.
word_sets = {
    "Animals": ["ant", "baboon", "badger", "bat", "bear", "beaver", "camel", "cat", "clam", "cobra"],
    "Shapes": ["square", "triangle", "rectangle", "circle", "ellipse", "rhombus", "trapezoid"],
    "Places": ["cairo", "london", "paris", "baghdad", "istanbul", "riyadh"]
}

# --- Database Functions ---
# These are the little helpers that will talk to our database.

def create_table():
    # This function makes sure our scoreboard exists. If not, it creates it.
    conn = sqlite3.connect('hangman_scores.db') # Connect to (or create) our database file.
    cursor = conn.cursor() # We use a 'cursor' to execute SQL commands.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            level TEXT PRIMARY KEY,
            winner_name TEXT,
            remaining_lives INTEGER
        )
    ''')
    # When we first create the table, let's put in some initial 'no score yet' values.
    default_scores = [('Easy', None, -1), ('Moderate', None, -1), ('Hard', None, -1)]
    cursor.executemany('''
        INSERT OR IGNORE INTO high_scores (level, winner_name, remaining_lives)
        VALUES (?, ?, ?)
    ''', default_scores)
    conn.commit() # Make sure our changes are saved.
    conn.close() # Close the connection to the database.

def get_high_scores():
    # This function fetches all the high scores from our database.
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT level, winner_name, remaining_lives FROM high_scores")
    scores = cursor.fetchall() # Get all the results.
    conn.close()
    return scores

def update_high_score(level, winner_name, remaining_lives):
    # This function updates the high score if the player did better than the current record.
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
    # This function shows off the best players!
    table = Texttable()
    table.header(["Level", "Winner name", "Remaining lives"])
    scores = get_high_scores()
    for level, winner, lives in scores:
        # If there's no winner yet, or no score, we show a nice '-'.
        table.add_row([level, winner if winner else "-", lives if lives != -1 else "-"])
    print(table.draw())

def display_about():
    # This function explains the game and its levels.
    print("\n" + "=" * 20)
    print("ABOUT THE GAME")
    print("=" * 20)
    print("Welcome to Hangman! Try to guess the secret word before you run out of lives.")
    print("\nLevel Challenges:")
    print("• Easy: You choose the category (Animals, Shapes, Places). 8 lives.")
    print("• Moderate: You choose the category (Animals, Shapes, Places). 6 lives.")
    print("• Hard: The computer chooses a random category and word. 6 lives. No hints!")
    print("\nHall of Fame:")
    print("See the top players and their remaining lives in the 'Hall of Fame' menu.")
    print("=" * 20)

def display_word_set_menu():
    # This menu lets the user pick a word set.
    table = Texttable()
    table.header(["Select a Set"])
    table.add_row(["Animals (1)"])
    table.add_row(["Shapes (2)"])
    table.add_row(["Places (3)"])
    print(table.draw())
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            return "Animals"
        elif choice == '2':
            return "Shapes"
        elif choice == '3':
            return "Places"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main_menu(player_name):
    # This is the main menu that greets the player.
    while True:
        table = Texttable()
        table.header([f"Hi {player_name}! Welcome to HANGMAN"])
        table.add_row(["PLAY THE GAME (1)"])
        table.add_row(["Hall of fame (4)"])
        table.add_row(["About the game (5)"])
        table.add_row(["Exit (0)"])
        print(table.draw())

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            play_game(player_name)
        elif choice == '4':
            display_hall_of_fame()
        elif choice == '5':
            display_about()
        elif choice == '0':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def play_game(player_name):
    # This function contains the core game logic.
    while True:
        table = Texttable()
        table.header(["Choose Difficulty"])
        table.add_row(["Easy level (1)"])
        table.add_row(["Moderate level (2)"])
        table.add_row(["Hard level (3)"])
        print(table.draw())

        difficulty_choice = input("Enter your choice: ").strip()

        if difficulty_choice in ['1', '2', '3']:
            if difficulty_choice == '1':
                difficulty = "Easy"
                lives = 8
                print("\nDifficulty: Easy (8 lives)")
                chosen_category = display_word_set_menu()
                selected_word_list = word_sets[chosen_category]
                secret_word = random.choice(selected_word_list)
                category_hint = f"Hint: The category is {chosen_category}."
                print(f"Okay, the word will be chosen from '{chosen_category}'.")

            elif difficulty_choice == '2':
                difficulty = "Moderate"
                lives = 6
                print(f"\nDifficulty: Moderate ({lives} lives)")
                chosen_category = display_word_set_menu()
                selected_word_list = word_sets[chosen_category]
                secret_word = random.choice(selected_word_list)
                category_hint = f"Hint: The category is {chosen_category}."
                print(f"Okay, the word will be chosen from '{chosen_category}'.")

            elif difficulty_choice == '3':
                difficulty = "Hard"
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

            while lives > 0:
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
                    print(f"Word: {' '.join(display_word)}")
                    print(f"\nCongratulations, {player_name}! You guessed the word: '{secret_word}'")
                    print("-----------------------------------")
                    update_high_score(difficulty, player_name, initial_lives - (initial_lives - lives))
                    break

            if lives == 0:
                print("\n-----------------------------------")
                print("\nGame Over! You ran out of lives.")
                print(f"The secret word was: '{secret_word}'")
                print("-----------------------------------")

            play_again = input("Do you want to play again? (yes/no): ").lower().strip()
            if play_again != 'yes':
                break # Go back to the main menu
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    main_menu(player_name) # Show the main menu again when the game loop ends

# --- Start the Game ---
if __name__ == "__main__":
    create_table() # Initialize the database
    player_name = input("Enter your name: ").strip()
    main_menu(player_name)
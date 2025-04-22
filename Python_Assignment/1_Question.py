import random
import time # Optional: To add slight pauses for dramatic effect

# --- Word Sets (keeping these the same) ---
word_sets = {
    "Animals": ["ant", "baboon", "badger", "bat", "bear", "beaver", "camel", "cat", "clam", "cobra"],
    "Shapes": ["square", "triangle", "rectangle", "circle", "ellipse", "rhombus", "trapezoid"],
    "Places": ["cairo", "london", "paris", "baghdad", "istanbul", "riyadh"]
}

# --- Hangman Graphics (Assuming you have these) ---
# Example: A list of ASCII art strings from empty to full hangman
stages = [
    # Stage 8 (Easy only - 8 lives left)
    '''
       +---+
       |   |
           |
           |
           |
           |
    ========= ''',
    # Stage 7 (Easy only - 7 lives left)
    '''
       +---+
       |   |
       O   |
           |
           |
           |
    ========= ''',
    # Stage 6 (6 lives left - Start for Mod/Hard, continue for Easy)
    '''
       +---+
       |   |
       O   |
       |   |
           |
           |
    ========= ''',
    # Stage 5 (5 lives left)
    '''
       +---+
       |   |
       O   |
      /|   |
           |
           |
    ========= ''',
    # Stage 4 (4 lives left)
    '''
       +---+
       |   |
       O   |
      /|\  |
           |
           |
    ========= ''',
    # Stage 3 (3 lives left)
    '''
       +---+
       |   |
       O   |
      /|\  |
      /    |
           |
    ========= ''',
    # Stage 2 (2 lives left)
    '''
       +---+
       |   |
       O   |
      /|\  |
      / \  |
           |
    ========= ''',
    # Stage 1 (1 life left) - Getting tense!
    '''
       +---+
       |   |
      (O)  |  <-- Uh oh!
      /|\  |
      / \  |
           |
    ========= ''',
    # Stage 0 (0 lives left) - Game Over
    '''
       +---+
       |   |
      (X)  |  <-- Game Over
      /|\  |
      / \  |
           |
    ========= '''
]

# --- Helper function for varied feedback ---
def get_random_feedback(kind):
    correct_feedback = ["Nice one!", "Got it!", "Yep, that's in there!", "Good eye!", "Exactly!"]
    incorrect_feedback = ["Nope, sorry!", "Not this time.", "That letter isn't hiding here.", "Ouch, that's a miss.", "Hmm, try another."]
    already_guessed_feedback = ["You already tried that one!", "Yep, you guessed that before. Still thinking...", "Pick a *new* letter!", "Deja vu? You guessed that already."]

    if kind == 'correct':
        return random.choice(correct_feedback)
    elif kind == 'incorrect':
        return random.choice(incorrect_feedback)
    elif kind == 'already_guessed':
        return random.choice(already_guessed_feedback)
    return ""


# --- Game Start ---
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("  Alright, let's play Hangman! ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# time.sleep(1) # Optional pause

# --- Difficulty Selection ---
while True:
    difficulty = input("How brave are you feeling? Choose a difficulty (Easy, Moderate, Hard): ").strip().capitalize()
    if difficulty in ["Easy", "Moderate", "Hard"]:
        break
    else:
        print("Heh, that's not an option. Please choose Easy, Moderate, or Hard.")

# --- Set Game Parameters Based on Difficulty ---
secret_word = ""
lives = 0
category_hint = ""
initial_lives = 0 # To know the starting point for graphics

if difficulty == "Easy":
    lives = 8
    initial_lives = 8
    print(f"\nOkay, Easy mode it is! Nice and relaxed. You'll have {lives} lives.")
    # time.sleep(0.5)
    print("First, pick your poison...")
    while True:
        print("\nAvailable categories:", ", ".join(word_sets.keys()))
        chosen_category = input("Which category do you want the word from?: ").strip().capitalize()
        if chosen_category in word_sets:
            selected_word_list = word_sets[chosen_category]
            secret_word = random.choice(selected_word_list)
            category_hint = f"Hint: Remember, we're thinking about {chosen_category}."
            print(f"Got it! I've picked a secret word from '{chosen_category}'.")
            break
        else:
            print(f"'{chosen_category}'? That's not on my list. Try one of these: {', '.join(word_sets.keys())}")

elif difficulty == "Moderate":
    lives = 6
    initial_lives = 6
    print(f"\nAlright, Moderate! A good challenge. Careful, only {lives} lives for this one.")
    # time.sleep(0.5)
    print("Let's see... which topic should the word be from?")
    while True:
        print("\nAvailable categories:", ", ".join(word_sets.keys()))
        chosen_category = input("Choose your category: ").strip().capitalize()
        if chosen_category in word_sets:
            selected_word_list = word_sets[chosen_category]
            secret_word = random.choice(selected_word_list)
            category_hint = f"Hint: The category is {chosen_category}."
            print(f"Okay, your word comes from the '{chosen_category}' category.")
            break
        else:
             print(f"'{chosen_category}'? Not an option right now. Choose from: {', '.join(word_sets.keys())}")

elif difficulty == "Hard":
    lives = 6
    initial_lives = 6
    print(f"\nOoh, Hard mode! Going for glory, are we? You've got {lives} lives.")
    # time.sleep(0.5)
    # Randomly select category and word
    random_category_name = random.choice(list(word_sets.keys()))
    selected_word_list = word_sets[random_category_name]
    secret_word = random.choice(selected_word_list)
    category_hint = "Hint: No category hints in Hard mode... it wouldn't be hard otherwise!"
    print("I've secretly picked a word from one of the categories. No peeking!")
    # time.sleep(1)

# --- Initialize Game State ---
guessed_letters = []
display_word = ["_"] * len(secret_word)

print("\nOkay, the word is set up. Let's get guessing!")
if category_hint:
    print(category_hint)
# time.sleep(1)

# --- Main Game Loop ---
while lives > 0:
    # Display current state
    print("\n-----------------------------------")
    # Adjust graphics display for different starting lives
    # We need to map the *remaining* lives to the correct stage index.
    # Stages are often drawn "in reverse" (index 0 is full hangman, highest index is empty)
    # Let's assume stages list is indexed 0 (lose) to 8 (start easy)
    # We need to find the correct index in the 'stages' list based on current 'lives'
    # If stages list has 9 elements (0-8):
    # Easy: lives 8..0 -> stages index 8..0 (direct mapping)
    # Mod/Hard: lives 6..0 -> stages index 6..0 (direct mapping, we just won't see 8 or 7)
    stage_index = lives # Assumes stages[0] is lose state, stages[max_lives] is start state
    if 0 <= stage_index < len(stages):
         print(stages[stage_index]) # Print the current hangman state
    else:
         print("      (Setting up...)") # Fallback if index is out of bounds

    print(f"\nWord: {' '.join(display_word)}")
    print(f"Letters you've tried: {', '.join(sorted(guessed_letters))}")
    #print(f"Lives left: {lives}") # Moved this after the guess result for better flow

    # Get guess
    guess = input("What's your guess? Enter a letter: ").lower().strip()

    # --- Input Validation ---
    if len(guess) != 1 or not guess.isalpha():
        print("Whoops! Just a single letter please, no numbers or symbols.")
        # time.sleep(0.5)
        continue
    if guess in guessed_letters:
        print(get_random_feedback('already_guessed'))
        # time.sleep(0.5)
        continue

    # Add valid, new guess to the list
    guessed_letters.append(guess)

    # --- Check Guess ---
    if guess in secret_word:
        print(f"-> {get_random_feedback('correct')} ('{guess}')")
        # Update display_word
        for i in range(len(secret_word)):
            if secret_word[i] == guess:
                display_word[i] = guess
    else:
        lives -= 1 # Lose a life *first*
        print(f"-> {get_random_feedback('incorrect')} ('{guess}')")
        print(f"   (Lives remaining: {lives})") # Show lives immediately after losing one
        # time.sleep(0.5)


    # --- Check Win Condition ---
    if "_" not in display_word:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Show final state (optional, could just show word)
        if 0 <= lives < len(stages): print(stages[lives])
        print(f"\nWord: {' '.join(display_word)}")
        print(f"\nYou did it! Amazing! The word was indeed '{secret_word}'!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break # Exit the loop on win

    # Loop continues if lives > 0 and word not fully guessed

# --- Check Loss Condition (executed if loop finishes without break) ---
if lives == 0:
    print("\n###################################")
    if 0 < len(stages): print(stages[0]) # Show the final losing stage
    print("\nOh no! You've run out of lives...")
    print(f"The word we were looking for was: '{secret_word}'")
    print("Better luck next time!")
    print("###################################")

# --- End of Game ---
print("\nThanks for playing Hangman!")
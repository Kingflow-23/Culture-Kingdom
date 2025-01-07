# Culture kingdom
#### Video Demo: 
https://youtu.be/8X5IuA3kI6M

#### Description:

This project is a console-based quiz game managed by an AI assistant named AI KF23. Players compete by answering questions of varying difficulties, earning points based on their answers. The game supports multiple players and allows for a customizable number of rounds and difficulty levels.

# Features

## Dynamic Player Management: 

Players can specify the number of participants and provide their names.

## Customizable Gameplay:

- Choose the number of rounds.
- Adjust difficulty for each round.

## Difficulty Levels:

- Easy: 1 point per correct answer.
- Medium: 2 points per correct answer.
- Hard: 3 points per correct answer.

## Real-time Scoring:

Scores are updated after each question.
The current score is displayed after each player's good answer.

## Final Rankings:

A detailed ranking of all players at the end of the game.
Handles ties gracefully, showing joint winners if applicable.

## Interactive gameplay:

Provides friendly and engaging prompts.
Guides players through the game rules and each round.

# Requirements

This project requires Python 3.8 or higher.

# Dependencies

Install the following Python libraries before running the project:
- requests: For fetching questions from the API.
- inflect: For generating human-readable rankings (e.g., "1st, 2nd, 3rd").

Install dependencies using:
pip install -r requirements.txt

# Configuration
The project uses a configuration file (config.py) to store the API URL for fetching trivia questions. Ensure the file contains:

API_URL = "https://opentdb.com/api.php?amount=10&type=multiple"

# How to Run
Clone or download the repository to your local machine.
Ensure all dependencies are installed (see above).

# Run the game with:

python project.py

# How the Game Works

## 1. Game Introduction
The game starts with a friendly introduction and rules explanation by AI KF23.

## 2. Setup Phase
- Specify the number of players.
- Provide player names.
- Set the number of rounds.

## 3. Gameplay
For each round:
- Players are asked to select a difficulty level: Easy, Medium, or Hard.
- Each player answers a question based on the chosen difficulty.
- Scores are updated in real-time based on correct answers.

## 4. Scoring
Points are awarded based on the difficulty level:
- Easy: 1 point.
- Medium: 2 points.
- Hard: 3 points.

## 5. Final Ranking
After all rounds, the game calculates the rankings.
- Handles ties by grouping tied players.
- Congratulates the winner(s) or joint winners.

# Functions Overview
Here’s a detailed explanation of the key functions:

## 1. game_opening()
Introduces the game to the players by displaying the rules and the structure of the game. It creates an engaging start to the game.
How It Works:
- Uses a formatted multi-line string to display an organized and visually appealing set of instructions.
- Includes details about:
    - How to set up the game.
    - Scoring rules.
    - Structure of each round.

## 2. get_num_players()
Asks the user to specify the number of players who will participate in the game. Ensures the input is valid.

Parameters:
    num_players (optional): An integer for testing or bypassing user input in automated scenarios.

How It Works:

- If num_players is provided:
    - It checks if it's a positive integer. If not, raises a ValueError.
- If not provided:
    - Continuously prompts the user for input until a valid positive integer is entered.
    - Handles invalid inputs (e.g., non-numeric or negative values) gracefully with error messages.
- Returns the valid number of players.

Example:

🤖 : How many players will be playing?
> two

❌❌ Invalid input. ❌❌

🤖 : Please enter a positive integer.
> 2

🤖 : Let's get started!

## 3. get_players(num_players: int)
Prompts players to enter their names and creates a list of player names.

Parameters:

num_players: The number of players (validated in get_num_players()).

How It Works:

- Iterates through the number of players.
- For each player:
    - Prompts the user for a name.
    - If the input is empty or whitespace, assigns a default name (e.g., "Player_1").
- Returns a list of player names.

Example:

🤖 : Enter the name of player 1:
> Alice

🤖 : Enter the name of player 2:
> 

🤖 : Player_2 will be your default name.

## 4. get_num_questions()
Asks the user for the number of rounds (questions) they’d like to play.

Parameters:

num_questions (optional): An integer for testing or bypassing user input in automated scenarios.

How It Works:

- If num_questions is provided:
    - Checks if it's a positive integer. If not, raises a ValueError.
- If not provided:
    - Continuously prompts the user for input until a valid positive integer is entered.
- Displays an error message for invalid inputs.

## 5. get_difficulty(difficulty_choice: str = "")
Allows players to choose the difficulty level for the questions in each round.

Parameters:

difficulty_choice (optional): A string (1, 2, or 3) for testing or bypassing user input.

How It Works:

- If difficulty_choice is provided:
    - Validates if it's "1" (easy), "2" (medium), or "3" (hard). Defaults to "easy" if invalid.
- If not provided:
    - Displays a menu with difficulty options.
    - Prompts the user for a choice and validates input.
- If no valid choice is made after 3 attempts, defaults to "easy".
- Returns the chosen difficulty level.

Example:

🤖 : Choose the difficulty level:
1. Easy
2. Medium
3. Hard
> 4

❌❌ Invalid choice. ❌❌

🤖 : Enter the number corresponding to your choice: 
> 2

## 6. clean_text(text: str)
Cleans text extracted from the trivia API by removing unwanted characters or HTML entities.

Parameters:

text: A string containing the raw text from the API.
How It Works:

- Replaces HTML entity \&amp; with &.
- Uses html.unescape to decode other HTML entities (e.g., \&lt; becomes <).

Example:

text = "What is 5 \&amp; 3?"
cleaned = clean_text(text)

Output: "What is 5 & 3?"

## 7. get_question(difficulty: str)
Fetches a trivia question from the API based on the chosen difficulty level.

Parameters:
- difficulty: The selected difficulty level ("easy", "medium", "hard").

How It Works:

- Sends a GET request to the trivia API (URL from config.py).
- Parses the JSON response to extract:
    - Question text.
    - Correct answer.
    - Incorrect answers.
    - Question category.
- Combines correct and incorrect answers, cleans them, and shuffles the order.
- Returns a tuple with the question, choices, correct answer, and category.

Error Handling:
- Retries if the API response is invalid or no questions match the difficulty.

## 8. ask_question(player: str, scores: dict, difficulty: str)
Asks a trivia question to the specified player and updates their score based on the answer.

Parameters:

- player: The current player's name.
- scores: A dictionary containing player scores.
- difficulty: The difficulty level of the question.

How It Works:

- Retrieves a question using get_question().
- Displays the question, choices, and category.
- Prompts the player to select an answer by number.
- Checks the answer:
    - If correct, updates the score using update_score() and congratulates the player.
    - If incorrect, displays the correct answer.
- Handles invalid inputs with error messages.

## 9. update_score(player: str, scores: dict, difficulty: str)
Calculates and updates the player’s score based on the question’s difficulty level.

Parameters:

- player: The player’s name.
- scores: The dictionary containing all players' scores.
- difficulty: The difficulty level of the question.

How It Works:

- Determines the point value:
    - Easy: 1 point.
    - Medium: 2 points.
    - Hard: 3 points.
- Adds the points to the player’s score in the dictionary.
- Displays the updated score.

## 10. display_final_ranking(scores: dict)
Displays the final rankings of players and announces the winner(s).

Parameters:

scores: A dictionary containing players and their total scores.

How It Works:

- Sorts the players by score in descending order.
- Handles ties:
    - Groups players with the same score.
    - Displays tied players together.
- Announces the winner(s).

Example:

--- Final Ranking ---
1st: Alice and Bob with 10 points
3rd: Charlie with 5 points
🤖 : Congratulations Alice and Bob! You are all joint winners! ✨

## 11. main()
Coordinates the entire game flow.

How It Works:

- Displays the introduction using game_opening().
- Gathers player and game setup data (get_num_players, get_players, get_num_questions).
- Manages rounds:
    - Loops through the number of questions.
    - Each round, all players take turns answering questions.
- Displays final rankings using display_final_ranking().

-----------------------------------------------------------------------------------
# Example Game Flow

🤖 : How many players will be playing?
> 2

🤖 : Enter the name of player 1:
> Alice

🤖 : Enter the name of player 2:
> Bob

🤖 : How many questions would you like to answer?
> 3

---------- Round 1 ----------

🤖 : Choose the difficulty level:
1. Easy
2. Medium
3. Hard
> 2

🤖 : Question of difficulty medium for Alice: What is the capital of France? (Category: Geography)
1. Paris
2. Berlin
3. Madrid
4. Rome
> 1

🤖 : Correct answer! ✅

Well done Alice ✨

🤖 : Alice earns 2 point(s). Total: 2 points

---------- Round 2 ----------

...

--- Final Ranking ---

1st: Alice with 5 points

2nd: Bob with 3 points

🤖 : Congratulations Alice! You are the overall winner! ✨

# Future Improvements
- Enhanced UI: Add colors for better readability using libraries like colorama.
- Custom API Options: Allow players to choose categories or question counts.
- Persistent Leaderboards: Save high scores locally or in a database for future sessions.
- Multiplayer Online Mode: Enable remote play over the internet.
- ...

# Contact

For questions or feedback, feel free to reach out:
- Email: florian.l.d.hounkpatin@gmail.com
- GitHub: @Kingflow-23

# Enjoy the game! 🎉
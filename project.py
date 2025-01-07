import re
import html
import random
import inflect
import requests
from config import *

api_url = API_URL


def game_opening() -> None:
    """
    Displays a opining message for the user to let him know about the game rules.
    """

    print(
        f"""
    Hello Everyone !! 
      
    I'm AI KF23 🤖, the game master of this game. 

    Let me introduce you to the rules ✨:

    - At the start of the game, you'll have to define the number of players.
    - Then, you'll be asked to give your name again for display reasons.
    - After that, you'll have to choose the number of rounds for our game.
     
    Each round contains one question, with a difficulty level set by the player for each one.
    
    The difficulty is asked again for each round, so you can change it if you want.
    Points are gained based on the difficulty level:
    - Easy: 1 point
    - Medium: 2 points
    - Hard: 3 points

    Overall points of players are displayed after each good answer.
      
    Please make sure to follow the instructions and have fun!! ✨  
    Let's all dive into the culture kingdom !! 🤖
    {"_"*100}
    """
    )


def get_num_players(num_players: int = 0) -> int:
    """
    Asks the user for the number of players who would like to play.

    Parameters:
        num_players (optionnal): The number of players. (for tests)

    Returns:
        num_players: The number of players.
    """
    if num_players:
        try:
            num_players = int(num_players)
            if num_players > 0:
                return num_players
            else:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid number of players") 
    else:
        while True:
            try:
                num_players = int(input("🤖 : How many players will be playing ? "))
                if num_players > 0:
                    print("\n🤖 : Let's get started!\n")
                    return num_players
            except ValueError:
                print(
                    "❌❌ Invalid input. ❌❌\n🤖 : Please enter a positive integer.\n"
                )


def get_num_questions(num_questions: int = 0) -> int:
    """
    Asks the user for the number of questions they'd like to play.

    Parameters:
        num_questions (optionnal): The number of questions the user wants to play. (for tests)

    Returns:
        num_questions: The number of questions the user wants to play.
    """
    if num_questions:
        try:
            num_questions = int(num_questions)
            if num_questions > 0:
                return num_questions
            else:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid number of questions")
    else:
        while True:
            try:
                num_questions = int(
                    input("\n🤖 : How many questions would you like to answer ? ")
                )
                if num_questions > 0:
                    return num_questions
            except ValueError:
                print(
                    "❌❌ Invalid input. ❌❌\n🤖 : Please enter a positive integer.\n"
                )


def get_players(num_players: int) -> list:
    """
    Asks the user for the names of the players.

    Args:
        num_players (int): The number of players.

    Returns:
        players: A list of player names.
    """
    players = []
    for i in range(num_players):
        name = input(f"🤖 : Enter the name of player {i + 1}: ")
        name = name if name.strip() != "" else f"Player_{i+1}"
        players.append(name)
    return players


def get_difficulty(difficulty_choice:str = "") -> str:
    """
    Asks the user for the difficulty level of the questions. (easy, medium, hard)

    Parameters:
        difficulty_choice (optionnal): The difficulty level of the questions as str(int). (for tests)

    Returns:
        difficulty: The difficulty level of the questions.
    """
    print("🤖 : Choose the difficulty level:")
    print("1. easy")
    print("2. medium")
    print("3. hard")
    if difficulty_choice and difficulty_choice in ["1", "2", "3"]:
        pass
    elif difficulty_choice and not difficulty_choice in ["1", "2", "3"]:
        raise ValueError("Invalid difficulty level")
    else:
        difficulty_choice = input("🤖 : Enter the number corresponding to your choice: ")

    for _ in range(2):
        if difficulty_choice == "1":
            return "easy"
        elif difficulty_choice == "2":
            return "medium"
        elif difficulty_choice == "3":
            return "hard"
        else:
            print("❌❌ Invalid choice. ❌❌\n")
            difficulty_choice = input(
                "🤖 : Enter the number corresponding to your choice: "
            )

    print("❌❌ Invalid choice. ❌❌\n🤖 : Defaulting to easy.")
    return "easy"


def clean_text(text: str) -> str:
    """
    Clean the text extrate from the API by removing any unwanted char.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    cleaned_text = re.sub(r"&amp;", "&", text)
    cleaned_text = html.unescape(text)

    return cleaned_text


def get_question(difficulty: str) -> tuple:
    """
    Retrieve informations about the question and the question itself from the API based on the difficulty level.

    Args:
        difficulty (str): The difficulty level of the question.

    Returns:
        tuple: A tuple containing the questions, choices, correct answer and the category.
    """
    while True:
        response = requests.get(api_url)

        if response.status_code != 200:
            # print(f"Failed to retrieve data: {response.status_code}")
            continue

        try:
            data = response.json()
            results = data["results"]
        except requests.exceptions.JSONDecodeError or IndexError:
            # print("Failed to decode JSON response")
            # print("Response content:", response.content)
            continue

        for result in results:
            if result["difficulty"] == difficulty:
                question = clean_text(result["question"])
                correct_answer = clean_text(result["correct_answer"])
                choices = result["incorrect_answers"]
                choices.append(correct_answer)
                choices = [clean_text(choice) for choice in choices]
                random.shuffle(choices)
                category = clean_text(result["category"])

                return (
                    question,
                    choices,
                    correct_answer,
                    category,
                )


def ask_question(player: str, scores: dict, difficulty: str) -> None:
    """
    Asks a question to the player and updates the scores dictionary accordingly.

    Args:
        player (str): The name of the player.
        scores (dict): A dictionary containing the scores of all players.
        difficulty (str): The difficulty level of the question.
    """
    question, choices, correct_answer, category = get_question(difficulty)
    print(
        f"\n🤖 : Question of difficulty {difficulty} for {player}: {question}, on subject {category}"
    )

    for i, choice in enumerate(choices):
        print(f"{i + 1}. {choice}")

    while True:
        try:
            answer = int(input("\n🤖 : Enter the number of your answer: "))
            if answer not in range(1, 5):
                raise ValueError
            if choices[answer - 1] == correct_answer:
                print(f"\n🤖 : Correct answer! ✅\nWell done {player} ✨")
                update_score(player, scores, difficulty)
                break
            else:
                print(
                    f"\n❌❌ Incorrect answer. ❌❌\n🤖 : The correct answer was: {correct_answer}"
                )
                break
        except (IndexError, ValueError):
            print(
                "❌❌ Incorrect answer. ❌❌\n🤖 : Please enter a number corresponding to one of the choices."
            )


def update_score(player: str, scores: dict, difficulty: str) -> None:
    """
    Updates the scores dictionary with the player's score for the given difficulty level.

    Args:
        player (str): The name of the player.
        scores (dict): A dictionary containing the scores of all players.
        difficulty (str): The difficulty level of the question.
    """

    if difficulty == "easy":
        points = 1
    elif difficulty == "medium":
        points = 2
    elif difficulty == "hard":
        points = 3
    else:
        points = 1

    scores[player] += points
    print(f"\n🤖 : {player} earns {points} point(s). \nTotal: {scores[player]} points")


def display_final_ranking(scores: dict) -> None:
    """
    Displays the final ranking of players. Handles ties by listing tied players together.

    Args:
        scores (dict): A dictionary containing the scores of all players.
    """
    p = inflect.engine()

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Final Ranking ---\n")
    print("🤖 : Let's see who's the ultimate champion!\n")

    rank = 1
    previous_score = None
    previous_rank = 1
    tied_players = []
    display_rank = 1

    for player, score in sorted_scores:
        if score == previous_score:
            tied_players.append(player)
            rank = previous_rank
        else:
            if tied_players:
                rank_text = p.ordinal(display_rank)
                player_text = p.join(tied_players)
                print(f"{rank_text}: {player_text} with {previous_score} points")
                display_rank = rank

                tied_players = []

            tied_players.append(player)
            previous_score = score
            previous_rank = rank

        rank += 1

    # If the last players in the sorted dict ties together.
    if tied_players:
        rank_text = p.ordinal(display_rank)
        player_text = p.join(tied_players)
        print(f"{rank_text}: {player_text} with {previous_score} points")

    tied_winners = [
        player for player, score in sorted_scores if score == sorted_scores[0][1]
    ]
    if len(tied_winners) > 1:
        winner_text = p.join(tied_winners)
        print(f"\n🤖 : Congratulations {winner_text} ! You are all joint winners! ✨")
    else:
        print(
            f"\n🤖 : Congratulations {tied_winners[0]} ! You are the overall winner! ✨"
        )


def main():

    game_opening()

    num_players = get_num_players()

    players = get_players(num_players)
    scores = {player: 0 for player in players}

    num_questions = get_num_questions()

    for round in range(num_questions):
        print(f"\n{'-'*10} Round {round + 1} {'-'*10}\n")

        difficulty = get_difficulty()

        for player in players:
            ask_question(player, scores, difficulty)

    print(f"\n{'-'*10} Game Over {'-'*10}")
    display_final_ranking(scores)


if __name__ == "__main__":
    main()

import cv2
import pygame
import inflect
import numpy as np
from config import *
from project import get_question

pygame.init()

# Load sounds
title_music_path = "Musics/title.mp3"
settings_music_path = "Musics/settings.mp3"
question_music_path = "Musics/question.wav"
result_sound = pygame.mixer.Sound("Musics/endgame.mp3")
correct_sound = pygame.mixer.Sound("Musics/correct.mp3")
incorrect_sound = pygame.mixer.Sound("Musics/incorrect.wav")

# Get the current screen size
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set the window size to match the screen size
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Culture Kingdom")

font = pygame.font.Font(None, FONT_SIZE)

# Background video paths
background_video_paths = {
    "menu": "Backgrounds/background_title.mp4",
    "settings": "Backgrounds/background_settings.mp4",
    "questions": "Backgrounds/background_question.mp4",
    "result": "Backgrounds/pre_result.mp4",
}

# Load background videos
background_videos = {
    state: cv2.VideoCapture(path) for state, path in background_video_paths.items()
}

STATE_MENU = 0
STATE_SETTINGS = 1
STATE_PLAY = 2
STATE_EXIT = 3


def get_video_frame(video_capture: cv2.VideoCapture) -> pygame.Surface:
    """
    Fetches the next frame from the given video capture object, looping back to the start if the video ends.

    Args:
        video_capture (cv2.VideoCapture): The video capture object to read frames from.

    Returns:
        pygame.Surface: The current video frame as a Pygame surface, or None if unable to read a frame.
    """
    ret, frame = video_capture.read()
    if not ret:  # Loop video if it ends
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
    return None


def display_video_frame_in_center(video_capture: cv2.VideoCapture) -> None:
    """
    Displays the current frame of the given video capture object, scaled to fit the entire screen.

    Args:
        video_capture (cv2.VideoCapture): The video capture object to display frames from.

    Returns:
        None
    """
    background_frame = get_video_frame(video_capture)

    if background_frame is not None:
        background_frame = pygame.transform.scale(
            background_frame, (screen_width, screen_height)
        )

        # Blit the background frame to cover the entire screen
        screen.blit(background_frame, (0, 0))


def display_text(
    text: str,
    x: int,
    y: int,
    color: tuple = BLACK,
    custom_font: pygame.font.Font = None,
    max_width: int = None,
) -> None:
    """ ""
    Displays text on the screen, with optional line wrapping if the text exceeds the specified maximum width.

    Args:
        text (str): The text to display.
        x (int): The x-coordinate of the top-left corner for the text.
        y (int): The y-coordinate of the top-left corner for the text.
        color (tuple): The color of the text (default is BLACK).
        custom_font (pygame.font.Font, optional): A custom font to use (default is the global font).
        max_width (int, optional): Maximum width of the text box for line wrapping.

    Returns:
        None
    """
    # Choose the font
    current_font = custom_font if custom_font else font

    # Split text into lines if max_width is provided
    if max_width:
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Test if adding the next word will exceed the width
            test_line = f"{current_line} {word}".strip()
            text_width, _ = current_font.size(test_line)

            if text_width <= max_width:
                # Add word to the current line
                current_line = test_line
            else:
                # Start a new line and add the current line to lines
                lines.append(current_line)
                current_line = word  # Start new line with the word that exceeded width

        # Add the last line
        if current_line:
            lines.append(current_line)
    else:
        # If max_width is not set, treat the entire text as a single line
        lines = [text]

    # Render each line and blit it with line spacing
    line_height = current_font.get_linesize()
    for i, line in enumerate(lines):
        rendered_text = current_font.render(line, True, color)
        screen.blit(rendered_text, (x, y + i * line_height))


def button(
    text: str,
    x: int,
    y: int,
    width: int,
    height: int,
    action=None,
    color: tuple = WHITE,
):
    """
    Displays an interactive button on the screen and handles click events.

    Args:
        text (str): The text displayed on the button.
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        width (int): The width of the button.
        height (int): The height of the button.
        action (Any, optional): The action to trigger when the button is clicked (default is None).
        color (tuple): The text color of the button (default is WHITE).

    Returns:
        Any: The value of `action` if the button is clicked, otherwise None.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, BLUE, (x, y, width, height))
        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(screen, BLACK, (x, y, width, height))

    display_text(text, x + 40, y + 30, color, custom_font=pygame.font.Font(None, 50))


def exit_button(color: tuple = WHITE):
    """
    Displays a pre-configured "Exit Game" button in the bottom-right corner of the screen.

    Args:
        color (tuple): The text color of the button (default is WHITE).

    Returns:
        Any: The action triggered by clicking the button (STATE_EXIT).
    """
    return button(
        "Exit Game",
        screen_width - BUTTON_WIDTH,
        screen_height - BUTTON_HEIGHT,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        STATE_EXIT,
        color=color,
    )


def back_button():
    """
    Displays a "Back" button in the bottom-left corner of the screen.

    Returns:
        Any: The action triggered by clicking the button (STATE_MENU).
    """
    return button(
        "Back",
        50,
        screen_height - BUTTON_HEIGHT,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        STATE_MENU,
    )


def main_menu() -> tuple:
    """
    Displays the main menu screen, allowing the user to choose between starting a new game,
    playing an unlimited solo game, or exiting the application.

    Returns:
        tuple: The next state of the game (STATE_SETTINGS or STATE_EXIT) and whether solo mode is selected (bool).
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(title_music_path)
    pygame.mixer.music.play(-1)

    video_capture = background_videos["menu"]

    title_font = pygame.font.Font(None, 150)

    pygame.display.flip()

    while True:
        display_video_frame_in_center(video_capture)

        display_text("Culture Kingdom", screen_width // 2 - 400, 175, RED, title_font)

        display_text(
            "King.Flow23", 20, screen_height - 80, WHITE, pygame.font.Font(None, 100)
        )

        if (
            button(
                "New Game",
                screen_width // 2 - BUTTON_WIDTH // 2,
                screen_height // 2 - 40,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                STATE_SETTINGS,
            )
            == STATE_SETTINGS
        ):
            pygame.mixer.music.stop()
            return STATE_SETTINGS, False

        if (
            button(
                "Unlimited Solo Game",
                screen_width // 2 - BUTTON_WIDTH // 2 - 75,
                screen_height // 2 + 100,
                BUTTON_WIDTH + 175,
                BUTTON_HEIGHT,
                STATE_SETTINGS,
            )
            == STATE_SETTINGS
        ):
            pygame.mixer.music.stop()
            return STATE_SETTINGS, True

        if exit_button() == STATE_EXIT:
            return STATE_EXIT, 0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT, 0


def game_settings(solo: bool = False) -> tuple:
    """
    Handles the settings screen where players can choose the number of players and rounds.

    Args:
        solo (bool): If True, sets the game to unlimited solo mode (default is False).

    Returns:
        tuple: The next state (STATE_PLAY, STATE_MENU, or STATE_EXIT), the list of player names,
               and the number of rounds (or -1 for unlimited rounds).
    """
    pygame.mixer.music.load(settings_music_path)
    pygame.mixer.music.play(-1)

    players = []
    num_players = 0
    num_questions = 0
    entering_players = True

    txt_font = pygame.font.Font(None, FONT_SIZE)

    settings_background = pygame.image.load("Backgrounds/pregame.jpg")
    settings_background = pygame.transform.scale(
        settings_background, (screen_width, screen_height)
    )

    while entering_players:
        screen.blit(settings_background, (0, 0))

        display_text(
            "Welcome to Culture Kingdom, our quiz game !!",
            175,
            50,
            BLACK,
            custom_font=txt_font,
        )

        if solo == False:
            display_text(
                "How many players are playing today ?",
                250,
                150,
                BLACK,
                custom_font=txt_font,
            )
        else:
            display_text(
                "Unlimited rounds! Play as long as you'd like. You can quit anytime.",
                50,
                150,
                BLACK,
                custom_font=txt_font,
                max_width=screen_width - 50,
            )
            num_players = 1

        if exit_button() == STATE_EXIT:
            return STATE_EXIT, [], 0

        if back_button() == STATE_MENU:
            pygame.mixer.music.stop()
            return STATE_MENU, [], 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and num_players > 0:
                    entering_players = False
                elif event.unicode.isdigit():
                    num_players = int(event.unicode)

        if num_players == 1 and solo == False:
            display_text(
                f"==> Seems like today, we'll only play with one player.",
                50,
                400,
                BLACK,
                custom_font=txt_font,
            )
        elif num_players > 0 and solo == False:
            display_text(
                f"==> So there'll be {num_players} players",
                50,
                400,
                BLACK,
                custom_font=txt_font,
            )

        pygame.display.flip()

    for i in range(num_players):
        player_name = ""
        entering_name = True

        while entering_name:
            screen.blit(settings_background, (0, 0))

            if exit_button() == STATE_EXIT:
                return STATE_EXIT, [], 0

            if back_button() == STATE_MENU:
                pygame.mixer.music.stop()
                return STATE_MENU, [], 0

            display_text(
                f"Please, enter a name for player {i + 1}: ",
                100,
                50,
                BLACK,
                custom_font=txt_font,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return STATE_EXIT

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name != "":
                        players.append(player_name)
                        entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

            display_text(
                f"==> Player {i + 1} name is: {player_name}",
                100,
                300,
                BLACK,
                custom_font=txt_font,
            )
            pygame.display.flip()

    entering_questions = True
    if solo == False:
        while entering_questions:
            screen.blit(settings_background, (0, 0))

            display_text(
                "Good now, choose the number of questions / rounds !!",
                50,
                50,
                BLACK,
                custom_font=txt_font,
            )

            if exit_button() == STATE_EXIT:
                return STATE_EXIT, [], 0

            if back_button() == STATE_MENU:
                pygame.mixer.music.stop()
                return STATE_MENU, [], 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return STATE_EXIT

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and num_questions > 0:
                        entering_questions = False
                    elif event.unicode.isdigit():
                        num_questions = int(event.unicode)

            if num_questions > 0:
                display_text(
                    f"Okay, today we are going to play on {num_questions} round(s)",
                    50,
                    300,
                    BLACK,
                    custom_font=txt_font,
                )

            pygame.display.flip()

    else:
        num_questions = -1

    return STATE_PLAY, players, num_questions


def play_game(players: list, num_questions: int):
    """
    Runs the main game loop where players answer questions and accumulate points.

    Args:
        players (list): List of player names.
        num_questions (int): Number of questions to be asked, or -1 for unlimited.

    Returns:
        Any: The next state of the game (STATE_MENU or STATE_EXIT).
    """
    EASY_POINT = 1
    MEDIUM_POINT = 2
    HARD_POINT = 3

    scores = {player: 0 for player in players}

    video_capture = background_videos["questions"]

    pygame.mixer.music.stop()
    pygame.mixer.music.load(question_music_path)
    pygame.mixer.music.play(-1)

    round_num = 0

    questions_num = num_questions

    if num_questions == -1:
        num_questions = 1

    while round_num < num_questions:
        for player in players:
            difficulty = choose_difficulty(player)

            if difficulty == STATE_MENU:
                return STATE_MENU
            elif difficulty == STATE_EXIT:
                return STATE_EXIT

            question, choices, correct_answer, category = get_question(difficulty)

            pygame.display.flip()

            asking = True
            selected = 0

            while asking:
                display_video_frame_in_center(video_capture)

                display_text(f"--- Round {round_num + 1} ---", 50, 50, WHITE)
                display_text(f"Difficulty : {difficulty.capitalize()}", 50, 100, WHITE)
                display_text(f"Subject : {category}", 50, 150, WHITE)
                display_text(f"Let's go {player} !!", 50, 250, WHITE)
                display_text(f"Score : {scores[player]}", screen_width - 350, 50, WHITE)
                display_text(question, 50, 350, WHITE, max_width=screen_width - 50)

                y = 500
                for i, choice in enumerate(choices):
                    color = BLUE if i == selected else WHITE
                    display_text(
                        f"{i + 1}. {choice}", 50, y, color, max_width=screen_width - 50
                    )
                    y += 80

                if exit_button() == STATE_EXIT:
                    return STATE_EXIT

                if back_button() == STATE_MENU:
                    pygame.mixer.music.stop()
                    return STATE_MENU

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return STATE_EXIT

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected = (selected - 1) % len(choices)
                        elif event.key == pygame.K_DOWN:
                            selected = (selected + 1) % len(choices)
                        elif event.key == pygame.K_RETURN:
                            asking = False
                            if choices[selected] == correct_answer:
                                if difficulty == "easy":
                                    scores[player] += EASY_POINT
                                    result_message = f"Correct! Well done {player}! Your good answer made you win {EASY_POINT} points."
                                elif difficulty == "medium":
                                    scores[player] += MEDIUM_POINT
                                    result_message = f"Correct! Well done {player}! Your good answer made you win {MEDIUM_POINT} points."
                                elif difficulty == "hard":
                                    scores[player] += HARD_POINT
                                    result_message = f"Correct! Well done {player}! Your good answer made you win {HARD_POINT} points."
                                correct_sound.play()
                                result_color = GREEN
                            else:
                                result_message = f"Incorrect! The correct answer was: {correct_answer}. You'll do better next time {player}."
                                incorrect_sound.play()
                                result_color = RED
                            break

            display_video_frame_in_center(video_capture)
            display_text(
                result_message, 50, 100, result_color, max_width=screen_width - 50
            )

            pygame.display.flip()
            pygame.time.wait(3000)

        round_num += 1

        if questions_num == -1:
            num_questions += 1

    return show_ranking(scores)


def choose_difficulty(player: str) -> str:
    """
    Allows a player to select the difficulty level for their question.

    Args:
        player (str): The name of the current player.

    Returns:
        str: The chosen difficulty level ('easy', 'medium', or 'hard').
    """
    selecting = True
    selected_difficulty = 0
    difficulties = ["easy", "medium", "hard"]

    while selecting:

        settings_background = pygame.image.load("Backgrounds/pregame.jpg")
        settings_background = pygame.transform.scale(
            settings_background, (screen_width, screen_height)
        )
        screen.blit(settings_background, (0, 0))

        display_text(f"{player}, choose your question difficulty !!", 50, 50, BLACK)

        y = 150
        for i, difficulty in enumerate(difficulties):
            color = BLUE if i == selected_difficulty else BLACK
            display_text(f"{i + 1}. {difficulty.capitalize()}", 50, y, color)
            y += 50

        if exit_button() == STATE_EXIT:
            return STATE_EXIT

        if back_button() == STATE_MENU:
            pygame.mixer.music.stop()
            return STATE_MENU

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    selecting = False

    return difficulties[selected_difficulty]


def show_ranking(scores: dict):
    """
    Displays the final ranking of players based on their scores and announces the winner.

    Args:
        scores (dict): A dictionary where keys are player names and values are their scores.

    Returns:
        Any: The next state of the game (STATE_MENU or STATE_EXIT).
    """
    pygame.mixer.music.stop()

    result_image = pygame.image.load("Backgrounds/results.jpg")
    video_capture = background_videos["result"]

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)

    p = inflect.engine()
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    wait_time = 3000
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < wait_time:
        display_video_frame_in_center(video_capture)
        pygame.time.delay(frame_delay)
        pygame.display.flip()

    result_sound.play()

    running = True

    while running:
        y = 100
        screen.blit(result_image, (0, 0))

        display_text("----- Final Ranking -----", 50, 50, BLUE)

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
                    display_text(
                        f"{rank_text}: {player_text} with {previous_score} points",
                        50,
                        y,
                        BLACK,
                    )
                    display_rank = rank

                    tied_players = []

                tied_players.append(player)
                previous_score = score
                previous_rank = rank

            rank += 1
            y += 50

        if tied_players:
            rank_text = p.ordinal(display_rank)
            player_text = p.join(tied_players)
            display_text(
                f"{rank_text}: {player_text} with {previous_score} points", 50, y, BLACK
            )
            y += 150

        tied_players = [
            player for player, score in sorted_scores if score == sorted_scores[0][1]
        ]
        if len(tied_players) > 1:
            player_text = p.join(tied_players)
            display_text(
                f"Congratulations {player_text} ! You are all joint winners!",
                50,
                y,
                GREEN,
            )
        else:
            display_text(
                f"Congratulations {tied_players[0]} ! You are the overall winner!",
                50,
                y,
                GREEN,
            )

        if back_button() == STATE_MENU:
            pygame.mixer.music.stop()
            return STATE_MENU

        if exit_button() == STATE_EXIT:
            running = False
            return STATE_EXIT

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT


def main() -> None:
    """
    The main entry point of the game, handling transitions between the menu, settings, game,
    and exit states.

    Returns:
        None
    """
    state = STATE_MENU

    while state != STATE_EXIT:
        if state == STATE_MENU:
            state, solo = main_menu()
        elif state == STATE_SETTINGS:
            state, players, num_questions = game_settings(solo)
        elif state == STATE_PLAY:
            state = play_game(players, num_questions)

    pygame.quit()


if __name__ == "__main__":
    main()

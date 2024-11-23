import os
import json
from hugchat import hugchat
from hugchat.login import Login

ASSISTANT_ID = "6741ea05b96dc97d6d15b237"

def list_cookie_files(cookie_dir):
    # list available cookie files
    if os.path.exists(cookie_dir):
        return [f for f in os.listdir(cookie_dir) if f.endswith('.json')]
    return []

def load_cookie_file(cookie_dir, file_name):
    # load the selected cookie file
    try:
        with open(os.path.join(cookie_dir, file_name), 'r') as f:
            cookies = json.load(f)
        return cookies
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading cookie file {file_name}: {e}")
        return None


def initialize_chatbot(email=None, password=None, cookie_dir='cookies'):
    # initialize by logging in using cookies or email&password
    # List available cookies
    cookie_files = list_cookie_files(cookie_dir)

    if cookie_files:
        print("Available cookie files:")
        for idx, file in enumerate(cookie_files, start=1):
            print(f"{idx}. {file}")

        while True:
            choice = input(f"Select a cookie file (1-{len(cookie_files)}) or press Enter to skip: ").strip()
            if not choice:
                print("Skipping cookie selection. Proceeding to email-password login...")
                break

            if choice.isdigit():
                selected_idx = int(choice) - 1
                if 0 <= selected_idx < len(cookie_files):
                    selected_file = cookie_files[selected_idx]
                    cookies = load_cookie_file(cookie_dir, selected_file)
                    if cookies:
                        print(f"Loaded cookies from {selected_file}")
                        return hugchat.ChatBot(cookies=cookies)
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(cookie_files)}.")
            else:
                print("Invalid input. Please enter a valid number.")

    # Prompt for email and password if skipping or no valid cookies
    if not email or not password:
        email = input("Enter your HuggingChat email: ").strip()
        password = input("Enter your HuggingChat password: ").strip()

    if email and password:
        try:
            login = Login(email, password)
            cookies = login.login(cookie_dir_path=cookie_dir, save_cookies=True)
            return hugchat.ChatBot(cookies=cookies.get_dict())
        except Exception as e:
            print(f"Error logging in: {str(e)}")
            exit()
    else:
        print("No valid login method found. Exiting.")
        exit()

# game loop
def start_game(chatbot):
    player_name = input("Enter your in-game character's name: ").strip()
    start_place = input("Enter a place where you would like to start the game: ").strip()
    print(f"Welcome to OpenRPG, {player_name}! The game will start soon. Please be patient.")

    #send initial setup message to the assistant
    setup_message = f"My name is {player_name}. Start the game in {start_place}."
    chatbot_response = chatbot.chat(setup_message)
    print(f"\n{chatbot_response}\n")
    while True:
        # get player input after chatbot's response
        player_action = input("What do you want to do?").strip()

        # send player input to chatbot
        if player_action.lower() in ['quit', 'exit']:
            print("Exiting OpenRPG. Thanks for playing!")
            break

        chatbot_response = chatbot.chat(player_action)

        # print chatbot's response
        print(f"\n{chatbot_response}\n")

        # check if chatbot says game over
        if "Game Over" in chatbot_response:
            print("Game Over!")
            print("Exiting OpenRPG...")
            break


def main():
    # Initialize chatbot using the helper function
    chatbot = initialize_chatbot(cookie_dir='cookies')

    if chatbot is None:
        print("Failed to initialize chatbot. Exiting...")
        return

    start_game(chatbot)


if __name__ == "__main__":
    main()
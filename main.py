import os
import json
from hugchat import hugchat
from hugchat.login import Login

ASSISTANT_ID = "673e2ad08a404f54ccb3a5e8"

#load sign in cookies from file
def load_cookies_from_file(cookie_file):
    try:
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)
        return cookies
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# log in and initialize
def initialize_chatbot(email=None, password=None, cookie_file='cookies.json'):
    # check if the cookies.json file exists in the current directory
    cookies = load_cookies_from_file(cookie_file)
    if cookies:
        print("Loaded cookies from cookies.json")
        chatbot = hugchat.ChatBot(cookies=cookies)
        return chatbot
    elif email and password:
        print("Logging in with email and password...")
        try:
            login = Login(email, password)
            cookies = login.login(cookie_dir_path='./cookies/', save_cookies=True)
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            return chatbot
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
            print("""  /$$$$$$                                           /$$$$$$                                /$$
                      /$$__  $$                                         /$$__  $$                              | $$
                     | $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$       | $$  \ $$ /$$    /$$ /$$$$$$   /$$$$$$ | $$
                     | $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$      | $$  | $$|  $$  /$$//$$__  $$ /$$__  $$| $$
                     | $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$      | $$  | $$ \  $$/$$/| $$$$$$$$| $$  \__/|__/
                     | $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/      | $$  | $$  \  $$$/ | $$_____/| $$          
                     |  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$      |  $$$$$$/   \  $/  |  $$$$$$$| $$       /$$
                      \______/  \_______/|__/ |__/ |__/ \_______/       \______/     \_/    \_______/|__/      |__/ """)
            print("Exiting OpenRPG...")
            break

# main function
def main():
    cookie_file = 'cookies.json'
    saved_account = '/cookies/*.json'
    if os.path.exists(cookie_file):
        # attempt to use cookies for login
        chatbot = initialize_chatbot(cookie_file=cookie_file)
    elif os.path.exists(saved_account):
        # attempt to use cookies for login
        chatbot = initialize_chatbot(cookie_file=saved_account)
    else:
        # fallback to email/password login if no cookie file exists/cookie file is invalid
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        chatbot = initialize_chatbot(email=email, password=password)
    start_game(chatbot)

if __name__ == "__main__":
    main()
# main.py
from chatbot.cli_bot import SimpleChatbot

def main():
    bot = SimpleChatbot(bot_name="LiaBot")
    bot.run_cli()

if __name__ == "__main__":
    main()

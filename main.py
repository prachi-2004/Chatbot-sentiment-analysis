#!/usr/bin/env python3
"""
Main entry point for the Chatbot with Sentiment Analysis
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot.cli_bot import SimpleChatbot

def main():
    """
    Main function to run the chatbot
    """
    try:
        # Initialize and run the chatbot
        bot = SimpleChatbot(bot_name="LiaBot")
        bot.run_cli()
    except KeyboardInterrupt:
        print("\n\nChatbot interrupted. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("Please ensure you have installed the required packages:")
        print("  pip install -r requirements.txt")
        print("Also, make sure NLTK data is downloaded:")
        print("  python -c \"import nltk; nltk.download('vader_lexicon')\"")
        sys.exit(1)

if __name__ == "__main__":
    main()
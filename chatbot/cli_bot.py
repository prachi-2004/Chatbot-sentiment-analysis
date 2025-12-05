# chatbot/cli_bot.py
from typing import List, Dict
from sentiment.analyzer import analyze_statement, conversation_level_sentiment, sentiment_trend

class SimpleChatbot:
    """
    Simple rule-based CLI chatbot that keeps conversation history and uses sentiment analyzer.
    """

    def __init__(self, bot_name: str = "LiaBot"):
        self.bot_name = bot_name
        self.history: List[Dict] = []  # list of dicts: {"speaker": "user"/"bot", "text": "..."}
        self.user_messages: List[str] = []
        self.system_messages: List[str] = []

    def add_user_message(self, text: str):
        self.history.append({"speaker": "user", "text": text})
        self.user_messages.append(text)

    def add_bot_message(self, text: str):
        self.history.append({"speaker": "bot", "text": text})
        self.system_messages.append(text)

    def bot_reply(self, user_text: str) -> str:
        """
        Example lightweight reply logic:
         - If user expresses gratitude -> friendly closing
         - If user expresses negative sentiment -> empathetic response
         - Otherwise echo with prompting question
        """
        info = analyze_statement(user_text)
        compound = info["compound"]
        if compound <= -0.5:
            reply = "I'm sorry you're feeling that way — would you like to tell me more so I can help?"
        elif compound < 0:
            reply = "I hear you — that sounds rough. Anything I can do to make it better?"
        elif compound >= 0.5:
            reply = "That's great to hear! What made it so good?"
        elif "thank" in user_text.lower():
            reply = "You're welcome! Anything else I can do?"
        else:
            # default: ask a follow-up
            reply = "Thanks for sharing. Can you tell me a little more about that?"

        self.add_bot_message(reply)
        return reply

    def run_cli(self):
        print(f"Welcome to {self.bot_name}! (type 'exit' or 'quit' to finish)\n")
        while True:
            try:
                txt = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nConversation ended by user.")
                break
            if not txt:
                continue
            if txt.lower() in ("exit", "quit"):
                print("Ending conversation and analyzing sentiment...\n")
                break
            self.add_user_message(txt)
            reply = self.bot_reply(txt)
            print(f"{self.bot_name}: {reply}\n")

        # On exit, run final reporting
        self.report()

    def report(self):
        print("----- Conversation Summary -----\n")
        # Show statement-level sentiment
        print("Statement-level sentiment (user messages):")
        for i, um in enumerate(self.user_messages):
            r = analyze_statement(um)
            print(f"{i+1}. User: \"{um}\" → Sentiment: {r['label']} (compound={r['compound']:.3f})")
        print()

        # Overall conversation sentiment
        conv = conversation_level_sentiment(self.user_messages, self.system_messages)
        print(f"Overall conversation sentiment: {conv['label']} (compound={conv['compound']:.3f})\n")

        # Trend summary
        trend = sentiment_trend(self.user_messages, window=2)
        if trend:
            print("Mood trend (moving window of size 2):")
            prev_label = None
            shifts = []
            for idx, label, avg in trend:
                print(f" Message {idx+1}: {label} (avg_compound={avg:.3f})")
                if prev_label is None:
                    prev_label = label
                elif label != prev_label:
                    shifts.append((idx+1, prev_label, label))
                    prev_label = label
            if shifts:
                print("\nDetected mood shifts:")
                for s in shifts:
                    print(f" - At message {s[0]}: {s[1]} → {s[2]}")
            else:
                print("\nNo significant mood shifts detected.")
        else:
            print("Not enough messages to compute trend.")
        print("\n----- End of Summary -----")

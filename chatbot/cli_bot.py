"""
Enhanced Chatbot with Sentiment Analysis
Features:
- Context-aware responses
- Multiple response templates
- Conversation memory
- Better sentiment integration
"""

import random
from typing import List, Dict, Optional
from datetime import datetime
import json

from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

from sentiment.analyzer import (
    analyze_statement, 
    conversation_level_sentiment, 
    sentiment_trend
)


class ResponseGenerator:
    """
    Handles chatbot response generation with context awareness
    """
    
    def __init__(self):
        self.response_templates = {
            'positive': [
                "That's wonderful to hear! 😊 What made your day so good?",
                "I'm so glad to hear that! 🌟 Tell me more!",
                "Fantastic! It's great to hear positive news.",
                "Awesome! What specifically made you feel happy?",
                "That's excellent! 🌈"
            ],
            'negative': [
                "I'm sorry you're feeling that way. 😔 Want to talk about it?",
                "That sounds tough. I'm here to listen if you want to share more.",
                "I understand it's hard. What can I do to support you?",
                "That must be challenging. Remember, it's okay to feel this way.",
                "I'm here for you. Take your time."
            ],
            'neutral': [
                "Thanks for sharing. What would you like to discuss?",
                "I understand. Tell me more about what's on your mind.",
                "Got it. What's happening with you today?",
                "Okay. How are you feeling about that?"
            ],
            'short_response': [
                "Got it. Tell me more.",
                "I see. What else is on your mind?",
                "Okay. What would you like to talk about?"
            ],
            'gratitude': [
                "You're welcome! 😊 Is there anything else I can help with?",
                "Glad I could help! Let me know if you need anything else.",
                "Happy to help! What's next for you today?"
            ],
            'stress_context': [
                "Stress can be overwhelming. Want to try a simple breathing exercise?",
                "I hear you're stressed. Sometimes taking a short break can help.",
                "That sounds challenging. Remember to be kind to yourself today."
            ],
            'improvement_context': [
                "That's great progress! Every step forward counts. 🎉",
                "Improvement takes time - you're doing amazing!",
                "Celebrate the small wins! You're moving in the right direction. 💪"
            ]
        }
    
    def get_response(self, user_text: str, sentiment_label: str, 
                    previous_context: Optional[str] = None) -> str:
        """
        Generate context-aware response based on sentiment and content
        
        Args:
            user_text: Current user message
            sentiment_label: Sentiment label from analyzer
            previous_context: Previous user message for context
            
        Returns:
            Appropriate bot response
        """
        user_text_lower = user_text.lower()
        
        # Check for specific patterns
        if "thank" in user_text_lower or "thanks" in user_text_lower:
            return random.choice(self.response_templates['gratitude'])
        
        # Check for short responses
        if len(user_text.split()) <= 2:
            # If it's a yes/no answer to a previous question
            if previous_context and ("?" in previous_context or 
                                   "can i" in previous_context.lower() or 
                                   "would you" in previous_context.lower()):
                if user_text_lower in ["yes", "yeah", "sure", "ok", "okay"]:
                    return "Great! Let's continue."
                elif user_text_lower in ["no", "nope", "not really"]:
                    return "Okay, no problem. What would you like to talk about instead?"
            return random.choice(self.response_templates['short_response'])
        
        # Check for specific contexts
        if any(word in user_text_lower for word in 
               ['stress', 'stressed', 'anxious', 'overwhelmed', 'pressure']):
            return random.choice(self.response_templates['stress_context'])
        
        if any(word in user_text_lower for word in 
               ['improving', 'better', 'progress', 'improvement', 'getting better']):
            return random.choice(self.response_templates['improvement_context'])
        
        # Sentiment-based responses
        if sentiment_label == "Positive":
            return random.choice(self.response_templates['positive'])
        elif sentiment_label == "Negative":
            return random.choice(self.response_templates['negative'])
        else:
            return random.choice(self.response_templates['neutral'])


class SimpleChatbot:
    """
    Enhanced chatbot with conversation history and sentiment analysis
    """
    
    def __init__(self, bot_name: str = "LiaBot"):
        self.bot_name = bot_name
        self.history: List[Dict] = []  # Full conversation history
        self.user_messages: List[Dict] = []  # User messages with metadata
        self.response_generator = ResponseGenerator()
        self.conversation_start_time = datetime.now()
        
        # Display welcome message
        self._print_welcome()
    
    def _print_welcome(self):
        """Print welcome banner"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"         Welcome to {self.bot_name}!")
        print("  (Type 'exit', 'quit', or press Ctrl+C to finish)")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Special commands:")
        print(f"  - 'summary': Show conversation summary")
        print(f"  - 'save': Save conversation to file")
        print(f"  - 'clear': Clear conversation history")
        print(f"{Style.RESET_ALL}")
    
    def add_message(self, speaker: str, text: str, sentiment: Optional[Dict] = None):
        """
        Add a message to history with metadata
        
        Args:
            speaker: 'user' or 'bot'
            text: Message text
            sentiment: Sentiment analysis results (for user messages)
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "text": text,
            "sentiment": sentiment
        }
        
        self.history.append(message)
        
        if speaker == "user":
            self.user_messages.append(message)
    
    def get_previous_user_message(self) -> Optional[str]:
        """Get the previous user message for context"""
        for msg in reversed(self.history):
            if msg["speaker"] == "user":
                return msg["text"]
        return None
    
    def bot_reply(self, user_text: str) -> str:
        """
        Generate bot response based on user input
        
        Args:
            user_text: User's message
            
        Returns:
            Bot's response
        """
        # Analyze sentiment
        sentiment_info = analyze_statement(user_text)
        
        # Get previous context
        previous_message = self.get_previous_user_message()
        
        # Generate response
        reply = self.response_generator.get_response(
            user_text, 
            sentiment_info["label"], 
            previous_message
        )
        
        # Add both messages to history
        self.add_message("user", user_text, sentiment_info)
        self.add_message("bot", reply)
        
        return reply, sentiment_info
    
    def get_conversation_summary(self) -> Dict:
        """Get comprehensive conversation summary"""
        user_texts = [msg["text"] for msg in self.user_messages]
        
        # Get overall sentiment (user messages only)
        overall_sentiment = conversation_level_sentiment(user_texts)
        
        # Get trend
        trend_data = sentiment_trend(user_texts, window=2)
        
        # Calculate statistics
        duration = datetime.now() - self.conversation_start_time
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        
        for msg in self.user_messages:
            if msg.get("sentiment"):
                label = msg["sentiment"]["label"]
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        
        return {
            "duration_seconds": duration.total_seconds(),
            "total_messages": len(self.history),
            "user_messages": len(self.user_messages),
            "bot_messages": len(self.history) - len(self.user_messages),
            "overall_sentiment": overall_sentiment,
            "sentiment_distribution": sentiment_counts,
            "trend_data": trend_data,
            "start_time": self.conversation_start_time.isoformat(),
            "end_time": datetime.now().isoformat()
        }
    
    def display_summary(self):
        """Display formatted conversation summary"""
        summary = self.get_conversation_summary()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print("               CONVERSATION SUMMARY")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        # Basic statistics
        print(f"\n{Fore.WHITE}📊 Conversation Statistics:")
        print(f"  Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"  Total messages: {summary['total_messages']}")
        print(f"  User messages: {summary['user_messages']}")
        print(f"  Bot messages: {summary['bot_messages']}")
        
        # Statement-level sentiment
        if self.user_messages:
            print(f"\n{Fore.WHITE}📝 Statement-level Sentiment Analysis:")
            for i, msg in enumerate(self.user_messages, 1):
                text = msg["text"]
                sentiment = msg.get("sentiment", {})
                label = sentiment.get("label", "N/A")
                compound = sentiment.get("compound", 0)
                
                # Choose color based on sentiment
                if label == "Positive":
                    color = Fore.GREEN
                    emoji = "😊"
                elif label == "Negative":
                    color = Fore.RED
                    emoji = "😔"
                else:
                    color = Fore.YELLOW
                    emoji = "😐"
                
                # Truncate long messages
                display_text = text if len(text) <= 50 else text[:47] + "..."
                print(f"  {i}. {color}{display_text}{Style.RESET_ALL}")
                print(f"     → {color}{label} {emoji} (score: {compound:.3f}){Style.RESET_ALL}")
        
        # Overall sentiment
        overall = summary["overall_sentiment"]
        print(f"\n{Fore.WHITE}🎯 Overall Conversation Sentiment:")
        
        if overall["label"] == "Positive":
            overall_color = Fore.GREEN
            overall_emoji = "😊"
        elif overall["label"] == "Negative":
            overall_color = Fore.RED
            overall_emoji = "😔"
        else:
            overall_color = Fore.YELLOW
            overall_emoji = "😐"
        
        print(f"  {overall_color}{overall['label']} {overall_emoji}")
        print(f"  Compound score: {overall_color}{overall['compound']:.3f}{Style.RESET_ALL}")
        
        # Sentiment distribution
        dist = summary["sentiment_distribution"]
        total_user = sum(dist.values())
        if total_user > 0:
            print(f"\n{Fore.WHITE}📈 Sentiment Distribution:")
            for label, count in dist.items():
                percentage = (count / total_user) * 100
                if label == "Positive":
                    bar = "▓" * int(percentage / 5)
                    color = Fore.GREEN
                elif label == "Negative":
                    bar = "▓" * int(percentage / 5)
                    color = Fore.RED
                else:
                    bar = "▓" * int(percentage / 5)
                    color = Fore.YELLOW
                
                print(f"  {label}: {color}{count} ({percentage:.1f}%) {bar}{Style.RESET_ALL}")
        
        # Mood trend
        trend = summary["trend_data"]
        if trend:
            print(f"\n{Fore.WHITE}📉 Mood Trend Analysis:")
            
            prev_label = None
            shifts = []
            
            for idx, label, avg in trend:
                if prev_label is None:
                    prev_label = label
                elif label != prev_label:
                    shifts.append((idx + 1, prev_label, label))
                    prev_label = label
            
            if shifts:
                print(f"  {Fore.CYAN}Detected mood shifts:{Style.RESET_ALL}")
                for shift_idx, from_label, to_label in shifts:
                    from_color = Fore.GREEN if from_label == "Positive" else Fore.RED if from_label == "Negative" else Fore.YELLOW
                    to_color = Fore.GREEN if to_label == "Positive" else Fore.RED if to_label == "Negative" else Fore.YELLOW
                    print(f"    - Message {shift_idx}: {from_color}{from_label}{Style.RESET_ALL} → {to_color}{to_label}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.CYAN}No significant mood shifts detected.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def save_conversation(self, filename: str = "conversation.json"):
        """Save conversation to JSON file"""
        try:
            data = {
                "conversation": self.history,
                "summary": self.get_conversation_summary(),
                "metadata": {
                    "bot_name": self.bot_name,
                    "export_time": datetime.now().isoformat()
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}✓ Conversation saved to '{filename}'{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving conversation: {e}{Style.RESET_ALL}")
            return False
    
    def run_cli(self):
        """Main CLI interaction loop"""
        print(f"\n{Fore.GREEN}💬 {self.bot_name} is ready. How can I help you today?{Style.RESET_ALL}")
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n{Fore.BLUE}You:{Style.RESET_ALL} ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Check for special commands
                user_input_lower = user_input.lower()
                
                if user_input_lower in ("exit", "quit", "bye"):
                    print(f"\n{Fore.YELLOW}Ending conversation and analyzing sentiment...{Style.RESET_ALL}")
                    break
                
                elif user_input_lower == "summary":
                    self.display_summary()
                    continue
                
                elif user_input_lower == "save":
                    self.save_conversation()
                    continue
                
                elif user_input_lower == "clear":
                    confirm = input(f"{Fore.YELLOW}Clear conversation history? (y/n): {Style.RESET_ALL}").strip().lower()
                    if confirm == 'y':
                        self.history = []
                        self.user_messages = []
                        self.conversation_start_time = datetime.now()
                        print(f"{Fore.GREEN}✓ Conversation cleared{Style.RESET_ALL}")
                    continue
                
                elif user_input_lower == "help":
                    print(f"{Fore.CYAN}Available commands:")
                    print(f"  - summary: Show conversation analysis")
                    print(f"  - save: Save conversation to file")
                    print(f"  - clear: Clear conversation history")
                    print(f"  - exit/quit/bye: End conversation")
                    print(f"  - help: Show this help message{Style.RESET_ALL}")
                    continue
                
                # Process user message
                reply, sentiment_info = self.bot_reply(user_input)
                
                # Display sentiment indicator
                label = sentiment_info["label"]
                if label == "Positive":
                    sent_color = Fore.GREEN
                    sent_emoji = "😊"
                elif label == "Negative":
                    sent_color = Fore.RED
                    sent_emoji = "😔"
                else:
                    sent_color = Fore.YELLOW
                    sent_emoji = "😐"
                
                print(f"  {sent_color}→ Sentiment: {label} {sent_emoji} (score: {sentiment_info['compound']:.3f}){Style.RESET_ALL}")
                
                # Display bot response
                print(f"\n{Fore.GREEN}{self.bot_name}:{Style.RESET_ALL} {reply}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrupted. Ending conversation...{Style.RESET_ALL}")
                break
            
            except EOFError:
                print(f"\n{Fore.YELLOW}End of input. Exiting...{Style.RESET_ALL}")
                break
        
        # End of conversation
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"              CONVERSATION COMPLETE")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        # Display summary
        self.display_summary()
        
        # Offer to save
        save_option = input(f"\n{Fore.YELLOW}Save conversation to file? (y/n): {Style.RESET_ALL}").strip().lower()
        if save_option == 'y':
            filename = input(f"{Fore.YELLOW}Filename (default: conversation.json): {Style.RESET_ALL}").strip()
            if not filename:
                filename = "conversation.json"
            self.save_conversation(filename)
        
        print(f"\n{Fore.GREEN}Thank you for chatting with {self.bot_name}! Goodbye! 👋{Style.RESET_ALL}")
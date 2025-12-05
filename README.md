# Chatbot-sentiment-analysis
A chatbot that conducts a conversation with a user and performs sentiment analysis.

# Chatbot with Sentiment Analysis (Tier 1 + Tier 2)

## 🚀 Project Overview
This project implements a simple conversational chatbot with sentiment analysis.

The chatbot:
- Maintains full conversation history  
- Performs sentiment analysis on each user message (**Tier 2**)  
- Computes overall conversation sentiment (**Tier 1**)  
- Summarizes mood trends across the conversation

✔ Tier 1 — Implemented  
✔ Tier 2 — Implemented  

---

## 🧰 How to Run the Project

### 1. Clone or download the project
```bash
git clone <your-repository-url>
cd chatbot-sentiment
2. Create and activate a virtual environment
Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
Mac/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install required dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the chatbot
bash
Copy code
python main.py
Type exit or quit anytime to end the chat and see the sentiment summary.

📦 Packages / Libraries Used
Library	Purpose
NLTK (VADER)	Sentiment analysis of messages
pytest	Optional testing
Python Standard Libraries	I/O handling, modular logic

VADER is chosen because it performs well on conversational text and detects sentiment in short sentences, slang, punctuation, and emojis.

🧠 Sentiment Analysis Method
🔹 1. Statement-Level Sentiment (Tier 2)
Each user message is analyzed using VADER:

It outputs:

pos (positive score)

neg (negative score)

neu (neutral score)

compound (overall score from -1 to +1)

Message is labeled using:

Positive → compound ≥ 0.05

Negative → compound ≤ -0.05

Neutral → otherwise

These sentiment labels are shown after conversation ends.

🔹 2. Conversation-Level Sentiment (Tier 1)
At the end of the chat:

Each message’s sentiment is calculated

A length-weighted average of compound scores is computed

The final sentiment label is assigned

Example:

yaml
Copy code
Overall sentiment: Negative (compound = -0.41)
🔹 3. Mood Trend (Optional Enhancement)
A moving average sentiment window (size = 2) is used to detect:

mood improvements

mood decline

mood shifts over time

Example:

mathematica
Copy code
Message 1 → Positive
Message 2 → Neutral
Mood shift detected: Positive → Neutral
🏆 Tier 2 Implementation Status
Tier 2 is fully implemented.
Per-message sentiment analysis + mood trend graphs are provided in the summary.

🧪 Running Tests
To run unit tests:

bash
Copy code
pytest -q
📁 Project Structure
css
Copy code
chatbot-sentiment/
├── main.py
├── README.md
├── requirements.txt
├── chatbot/
│   └── cli_bot.py
├── sentiment/
│   └── analyzer.py
└── tests/
    └── test_sentiment.py

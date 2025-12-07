# **Chatbot with Sentiment Analysis**
*A Python-based chatbot that conducts conversations with users and performs real-time sentiment analysis.*

## 📋 **Project Overview**
This project implements a conversational chatbot with comprehensive sentiment analysis capabilities. The system maintains complete conversation history and analyzes emotional tone at both individual statement and overall conversation levels.

### **Implementation Status**
| Requirement | Status | Description |
|------------|--------|-------------|
| **Tier 1** | ✅ **Fully Implemented** | Conversation-level sentiment analysis with clear emotional direction |
| **Tier 2** | ✅ **Fully Implemented** | Statement-level analysis for every user message with mood trend detection |

## 🚀 **How to Run**

### **Prerequisites**
- Python 3.7 or higher
- pip (Python package manager)

### **Installation Steps**

1. **Clone or download the project:**
```bash
git clone <(https://github.com/prachi-2004/Chatbot-sentiment-analysis.git)>
cd chatbot-sentiment-analysis
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data (first run only):**
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

5. **Run the chatbot:**
```bash
python main.py
```

6. **Type `exit`, `quit`, or `bye` anytime to end the chat and see the sentiment summary.**

## 🛠 **Chosen Technologies**

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.7+ |
| **NLTK VADER** | Sentiment analysis engine | 3.8.1 |
| **Colorama** | Colored terminal output | 0.4.6 |
| **pytest** | Testing framework (optional) | 7.4.3 |
| **JSON** | Conversation persistence | Built-in |

### **Why VADER?**
- **Optimized for conversational text**: Handles slang, emoticons, and informal language
- **Rule-based**: No training data required
- **Context-aware**: Considers punctuation, capitalization, and degree modifiers
- **Fast and lightweight**: Real-time analysis without heavy computational requirements

## 🧠 **Sentiment Analysis Logic**

### **1. Statement-Level Analysis (Tier 2)**
Each user message is analyzed in real-time using VADER sentiment analyzer:

```python
# For each user message:
scores = {
    "compound": -0.542,  # Overall score (-1 to +1)
    "neg": 0.623,        # Negative sentiment proportion
    "neu": 0.377,        # Neutral sentiment proportion  
    "pos": 0.000,        # Positive sentiment proportion
    "label": "Negative"   # Sentiment classification
}
```

**Classification thresholds:**
- **Positive** → `compound ≥ 0.05`
- **Negative** → `compound ≤ -0.05`  
- **Neutral** → All other values

**Real-time display:**
```
You: "I'm feeling stressed today"
→ Sentiment: Negative 😔 (score: -0.421)
```

### **2. Conversation-Level Analysis (Tier 1)**
At conversation end, overall sentiment is calculated using **weighted averaging**:

```python
# Weighted by message length to reduce bias
overall_compound = Σ(message_compound × word_count^0.5) / Σ(word_count^0.5)
```

**Output format:**
```
Overall conversation sentiment: Positive (compound: 0.122)
```

### **3. Mood Trend Analysis (Enhanced Feature)**
Tracks emotional progression throughout the conversation:

- **Moving window analysis** (default: window size = 2)
- **Shift detection**: Identifies exact points where mood changes
- **Visual trend representation**: ASCII bars show sentiment distribution

**Example output:**
```
📉 Mood Trend Analysis:
Detected mood shifts:
 - At message 3: Negative → Positive
```

## ✅ **Tier 2 Implementation Status**

### **Fully Implemented Features:**

| Feature | Status | Details |
|---------|--------|---------|
| **Per-message analysis** | ✅ Complete | Every user message analyzed individually |
| **Real-time display** | ✅ Complete | Sentiment shown immediately after each message |
| **Detailed scoring** | ✅ Complete | Compound score + individual emotion scores |
| **Trend visualization** | ✅ Complete | Moving window analysis with shift detection |
| **Context-aware responses** | ✅ Complete | Bot responses vary based on detected sentiment |

### **Enhanced Tier 2 Features:**
1. **Multiple response templates**: Different responses for positive, negative, and neutral sentiments
2. **Context detection**: Identifies specific topics (stress, improvement, gratitude)
3. **Short message handling**: Special logic for "yes", "no", and other brief responses
4. **Conversation memory**: References previous messages for coherent responses

## 🧪 **Testing**

### **Test Suite Structure**
```
tests/
└── test_sentiment.py
    ├── Unit Tests: Individual function testing
    ├── Integration Tests: Complete workflow testing  
    └── Edge Cases: Empty strings, boundary conditions
```

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python tests/test_sentiment.py

# Example output:
# test_analyze_statement_positive PASSED
# test_analyze_statement_negative PASSED
# test_conversation_level_sentiment PASSED
# ✅ All tests passed!
```

## 📁 **Project Structure**

```
chatbot-sentiment/
├── main.py                 # Entry point - launches the chatbot
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── chatbot/
│   └── cli_bot.py         # Chatbot logic, CLI interface, response generation
├── sentiment/
│   └── analyzer.py        # Core sentiment analysis functions
└── tests/
    └── test_sentiment.py  # Comprehensive test suite
```

### **Module Responsibilities:**
- **`main.py`**: Application entry point and error handling
- **`chatbot/cli_bot.py`**: Manages conversation flow, user interaction, and response logic
- **`sentiment/analyzer.py`**: Pure sentiment analysis functions (reusable, testable)
- **`tests/test_sentiment.py`**: Unit and integration tests

## 💬 **Example Conversations**

### **Example 1: Basic Sentiment Analysis**
```
You: "Your service disappoints me"
→ Sentiment: Negative 😔 (score: -0.421)
LiaBot: "I'm sorry to hear that. 😔 Want to talk about it?"

You: "Last experience was better"
→ Sentiment: Positive 😊 (score: 0.334)
LiaBot: "That's great to hear! 🌟 Tell me more!"

Type 'summary':
Overall conversation sentiment: Negative – general dissatisfaction
```

### **Example 2: Complete Conversation with Analysis**
```
You: I had a terrible morning
→ Sentiment: Negative 😔 (score: -0.612)
LiaBot: That sounds tough. I'm here to listen.

You: But lunch with friends helped
→ Sentiment: Positive 😊 (score: 0.445)  
LiaBot: That's wonderful to hear! 😊 What made it so good?

You: I'm feeling much better now
→ Sentiment: Positive 😊 (score: 0.521)
LiaBot: Awesome! Keep riding that positive wave!

Type 'quit':

📊 CONVERSATION SUMMARY:
- Statement-level analysis: 3 messages with individual sentiment scores
- Overall sentiment: Positive (compound: 0.118)
- Mood trend: Negative → Positive (shift at message 2)
- Distribution: Positive 67%, Negative 33%
```

### **Available Commands During Chat:**
- `summary` – Show conversation analysis
- `save` – Save conversation to JSON file  
- `clear` – Clear conversation history
- `help` – Show available commands
- `exit`/`quit`/`bye` – End conversation

## ✨ **Innovations & Additional Features**

### **1. Enhanced User Experience**
- **Color-coded interface**: Visual sentiment indicators (green/red/yellow)
- **Emoji feedback**: Quick emotional recognition
- **Progress bars**: ASCII visualization of sentiment distribution
- **Real-time feedback**: Immediate sentiment display after each message

### **2. Production-Ready Features**
- **Conversation persistence**: Auto-save to JSON with full metadata
- **Error handling**: Graceful degradation with user-friendly messages
- **Modular architecture**: Separated concerns for maintainability
- **Configurable thresholds**: Easy adjustment of sentiment boundaries

### **3. Advanced Analytics**
- **Weighted averaging**: Message length considered in overall sentiment
- **Statistical breakdown**: Percentages, averages, standard deviation
- **Trend visualization**: Clear display of mood progression
- **Export capabilities**: JSON format for further analysis

### **4. Context-Aware Responses**
- **Multiple templates**: Different responses for each sentiment category
- **Keyword detection**: Identifies specific contexts (stress, improvement)
- **Conversation memory**: References previous messages
- **Appropriate follow-ups**: Asks relevant questions based on sentiment

## 📄 **Output Files**
Conversations are automatically saved to `conversation.json` when you type `save` or end the chat. The file includes:
- Full conversation history with timestamps
- Sentiment analysis for each user message
- Overall conversation statistics
- Metadata (duration, message counts, export time)

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **NLTK data not found**: Run `python -c "import nltk; nltk.download('vader_lexicon')"`
2. **Import errors**: Ensure virtual environment is activated
3. **Color issues**: Install colorama with `pip install colorama`

### **Testing Your Installation:**
```bash
# Test Python environment
python --version

# Test NLTK installation
python -c "import nltk; print('NLTK version:', nltk.__version__)"

# Test sentiment analyzer
python -c "from sentiment.analyzer import analyze_statement; print(analyze_statement('I love this!'))"
```

## 📚 **References**
- **VADER Sentiment Analysis**: [NLTK Documentation](https://www.nltk.org/howto/sentiment.html)
- **Python NLTK**: [Official Website](https://www.nltk.org/)
- **Colorama**: [GitHub Repository](https://github.com/tartley/colorama)

## 📄 **License**
This project was developed as part of the LiaPlus Assignment for educational purposes.

---

**Ready to chat?** Run `python main.py` and start your conversation with sentiment-aware LiaBot!

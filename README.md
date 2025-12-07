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
## 💬 **Example Conversations**

### **Example : Complete Conversation with Analysis**
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

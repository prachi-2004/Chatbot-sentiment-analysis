# tests/test_sentiment.py
from sentiment.analyzer import analyze_statement, conversation_level_sentiment, sentiment_trend

def test_analyze_statement_positive():
    r = analyze_statement("I love this product, it's fantastic!")
    assert r["label"] == "Positive"
    assert r["compound"] > 0.5

def test_analyze_statement_negative():
    r = analyze_statement("This is horrible, I hate it.")
    assert r["label"] == "Negative"
    assert r["compound"] < -0.5

def test_conversation_level_sentiment_mixture():
    users = ["I love it", "But last time was bad", "Now it's okay"]
    conv = conversation_level_sentiment(users)
    assert "label" in conv
    assert isinstance(conv["compound"], float)

def test_trend_length():
    users = ["Good", "Bad", "Fine"]
    trend = sentiment_trend(users, window=2)
    assert len(trend) == len(users)

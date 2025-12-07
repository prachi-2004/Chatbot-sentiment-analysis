"""
Comprehensive tests for sentiment analysis module
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sentiment.analyzer import (
    analyze_statement,
    label_from_compound,
    conversation_level_sentiment,
    sentiment_trend,
    get_sentiment_statistics,
    detect_mood_shifts,
    POSITIVE_THRESHOLD,
    NEGATIVE_THRESHOLD
)


class TestSentimentAnalyzer:
    """Test suite for sentiment analysis functions"""
    
    def test_analyze_statement_positive(self):
        """Test positive sentiment analysis"""
        result = analyze_statement("I love this product, it's absolutely fantastic!")
        
        assert "text" in result
        assert "compound" in result
        assert "label" in result
        assert result["label"] == "Positive"
        assert result["compound"] > POSITIVE_THRESHOLD
        assert 0 <= result["neg"] <= 1
        assert 0 <= result["neu"] <= 1
        assert 0 <= result["pos"] <= 1
        
        # Check that scores sum to approximately 1
        total = result["neg"] + result["neu"] + result["pos"]
        assert 0.99 <= total <= 1.01  # Allow small floating point errors
    
    def test_analyze_statement_negative(self):
        """Test negative sentiment analysis"""
        result = analyze_statement("This is horrible, I hate it so much.")
        
        assert result["label"] == "Negative"
        assert result["compound"] < NEGATIVE_THRESHOLD
        assert result["neg"] > 0  # Should have some negative score
    
    def test_analyze_statement_neutral(self):
        """Test neutral sentiment analysis"""
        result = analyze_statement("The weather is okay today.")
        
        assert result["label"] == "Neutral"
        assert NEGATIVE_THRESHOLD <= result["compound"] <= POSITIVE_THRESHOLD
    
    def test_analyze_statement_empty(self):
        """Test empty string handling"""
        result = analyze_statement("")
        
        assert result["label"] == "Neutral"
        assert result["compound"] == 0.0
        assert result["neu"] == 1.0
        assert result["neg"] == 0.0
        assert result["pos"] == 0.0
    
    def test_analyze_statement_whitespace(self):
        """Test whitespace-only string"""
        result = analyze_statement("   ")
        
        assert result["label"] == "Neutral"
        assert result["compound"] == 0.0
    
    def test_label_from_compound(self):
        """Test compound score to label conversion"""
        # Test positive thresholds
        assert label_from_compound(0.5) == "Positive"
        assert label_from_compound(0.05) == "Positive"  # Edge case
        assert label_from_compound(0.049) == "Neutral"  # Just below threshold
        
        # Test negative thresholds
        assert label_from_compound(-0.5) == "Negative"
        assert label_from_compound(-0.05) == "Negative"  # Edge case
        assert label_from_compound(-0.049) == "Neutral"  # Just above threshold
        
        # Test neutral range
        assert label_from_compound(0.0) == "Neutral"
        assert label_from_compound(0.03) == "Neutral"
        assert label_from_compound(-0.03) == "Neutral"
    
    def test_label_from_compound_custom_thresholds(self):
        """Test with custom thresholds"""
        # Custom stricter thresholds
        assert label_from_compound(0.1, pos_thresh=0.1, neg_thresh=-0.1) == "Positive"
        assert label_from_compound(0.09, pos_thresh=0.1, neg_thresh=-0.1) == "Neutral"
        assert label_from_compound(-0.1, pos_thresh=0.1, neg_thresh=-0.1) == "Negative"
        assert label_from_compound(-0.09, pos_thresh=0.1, neg_thresh=-0.1) == "Neutral"
    
    def test_conversation_level_sentiment_empty(self):
        """Test empty conversation"""
        result = conversation_level_sentiment([])
        
        assert result["compound"] == 0.0
        assert result["label"] == "Neutral"
        assert result["message_count"] == 0
        assert len(result["details"]) == 0
    
    def test_conversation_level_sentiment_single(self):
        """Test single message conversation"""
        result = conversation_level_sentiment(["I love this!"])
        
        assert result["message_count"] == 1
        assert len(result["details"]) == 1
        assert result["details"][0]["text"] == "I love this!"
        assert result["weighted_average"] == True
    
    def test_conversation_level_sentiment_mixed(self):
        """Test mixed sentiment conversation"""
        messages = [
            "I love this!",
            "This is terrible",
            "It's okay I guess"
        ]
        
        result = conversation_level_sentiment(messages)
        
        assert result["message_count"] == 3
        assert len(result["details"]) == 3
        assert "compound" in result
        assert "label" in result
        
        # Check all messages are in details
        detail_texts = [d["text"] for d in result["details"]]
        assert all(msg in detail_texts for msg in messages)
    
    def test_conversation_level_sentiment_ignores_system(self):
        """Test that system messages are not included in calculation"""
        user_messages = ["I'm happy"]
        system_messages = ["Hello!", "How can I help?"]
        
        result = conversation_level_sentiment(user_messages, system_messages)
        
        # Should only have 1 message (user message)
        assert result["message_count"] == 1
        assert len(result["details"]) == 1
        assert result["details"][0]["text"] == "I'm happy"
    
    def test_sentiment_trend_empty(self):
        """Test trend analysis with empty list"""
        result = sentiment_trend([])
        assert result == []
    
    def test_sentiment_trend_single(self):
        """Test trend analysis with single message"""
        result = sentiment_trend(["Good day"])
        
        assert len(result) == 1
        assert result[0][0] == 0  # Index
        assert isinstance(result[0][1], str)  # Label
        assert isinstance(result[0][2], float)  # Average compound
    
    def test_sentiment_trend_multiple(self):
        """Test trend analysis with multiple messages"""
        messages = ["Good", "Bad", "Great"]
        result = sentiment_trend(messages, window=2)
        
        assert len(result) == len(messages)
        
        # Check structure of each tuple
        for idx, label, avg in result:
            assert isinstance(idx, int)
            assert isinstance(label, str)
            assert isinstance(avg, float)
            assert label in ["Positive", "Negative", "Neutral"]
    
    def test_sentiment_trend_different_windows(self):
        """Test trend analysis with different window sizes"""
        messages = ["A", "B", "C", "D", "E"]
        
        # Test window = 1 (no averaging)
        result1 = sentiment_trend(messages, window=1)
        assert len(result1) == 5
        
        # Test window = 3
        result3 = sentiment_trend(messages, window=3)
        assert len(result3) == 5
        
        # Test window larger than message count
        result10 = sentiment_trend(messages, window=10)
        assert len(result10) == 5
    
    def test_get_sentiment_statistics(self):
        """Test sentiment statistics calculation"""
        messages = [
            "I love this!",
            "This is bad",
            "It's okay"
        ]
        
        stats = get_sentiment_statistics(messages)
        
        assert stats["total_messages"] == 3
        assert sum(stats["sentiment_counts"].values()) == 3
        
        # Check percentages
        for label, percentage in stats["percentages"].items():
            assert 0 <= percentage <= 100
        
        # Check average compound is within valid range
        assert -1 <= stats["average_compound"] <= 1
        
        # Check standard deviation is non-negative
        assert stats["compound_std"] >= 0
    
    def test_detect_mood_shifts_empty(self):
        """Test mood shift detection with empty list"""
        shifts = detect_mood_shifts([])
        assert shifts == []
    
    def test_detect_mood_shifts_single(self):
        """Test mood shift detection with single message"""
        shifts = detect_mood_shifts(["Hello"])
        assert shifts == []
    
    def test_detect_mood_shifts_actual(self):
        """Test actual mood shift detection"""
        messages = [
            "I'm very sad today",
            "Actually, I'm feeling better now",
            "This is fantastic!"
        ]
        
        shifts = detect_mood_shifts(messages, min_change=0.1)
        
        # Should detect at least one shift
        assert len(shifts) >= 1
        
        # Check shift structure
        for shift in shifts:
            assert "message_index" in shift
            assert "from_label" in shift
            assert "to_label" in shift
            assert "change_magnitude" in shift
            assert "description" in shift
            assert shift["change_magnitude"] >= 0.1


def test_integration_workflow():
    """Test complete workflow from single analysis to conversation summary"""
    # Test data
    conversation = [
        "I started the day feeling anxious",
        "But then I had a good meeting",
        "Now I'm feeling much better"
    ]
    
    # Step 1: Analyze individual statements
    analyses = [analyze_statement(msg) for msg in conversation]
    
    # All should have valid sentiment labels
    for analysis in analyses:
        assert analysis["label"] in ["Positive", "Negative", "Neutral"]
    
    # Step 2: Get conversation-level sentiment
    conv_sentiment = conversation_level_sentiment(conversation)
    assert "label" in conv_sentiment
    assert "compound" in conv_sentiment
    
    # Step 3: Analyze trend
    trend = sentiment_trend(conversation)
    assert len(trend) == len(conversation)
    
    # Step 4: Get statistics
    stats = get_sentiment_statistics(conversation)
    assert stats["total_messages"] == len(conversation)
    
    # Step 5: Detect shifts
    shifts = detect_mood_shifts(conversation)
    # Might or might not detect shifts depending on thresholds
    assert isinstance(shifts, list)
    
    print("✓ All integration tests passed")


if __name__ == "__main__":
    # Run tests manually if needed
    print("Running sentiment analysis tests...")
    
    test_suite = TestSentimentAnalyzer()
    
    # Run basic tests
    test_suite.test_analyze_statement_positive()
    print("✓ Positive sentiment test passed")
    
    test_suite.test_analyze_statement_negative()
    print("✓ Negative sentiment test passed")
    
    test_suite.test_analyze_statement_neutral()
    print("✓ Neutral sentiment test passed")
    
    test_suite.test_conversation_level_sentiment_mixed()
    print("✓ Mixed conversation test passed")
    
    test_suite.test_sentiment_trend_multiple()
    print("✓ Trend analysis test passed")
    
    # Run integration test
    test_integration_workflow()
    
    print("\n✅ All tests passed successfully!")
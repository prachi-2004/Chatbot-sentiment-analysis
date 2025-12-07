"""
Sentiment Analysis Module using NLTK VADER
Corrected version with proper error handling and consistent thresholds
"""

import os
import sys
from typing import List, Dict, Tuple, Optional

# Try to import NLTK, provide helpful error if not installed
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    print("Error: NLTK is not installed. Please install it with:")
    print("  pip install nltk")
    sys.exit(1)

# Constants for sentiment thresholds
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

# Global analyzer instance
_sia = None

def _ensure_vader_lexicon():
    """
    Ensure VADER lexicon is downloaded.
    Handles download with user-friendly error messages.
    """
    global _sia
    
    try:
        # Try to find the lexicon
        nltk.data.find('sentiment/vader_lexicon.zip')
        _sia = SentimentIntensityAnalyzer()
    except LookupError:
        print("VADER lexicon not found. Downloading...")
        try:
            nltk.download('vader_lexicon', quiet=False)
            _sia = SentimentIntensityAnalyzer()
            print("VADER lexicon downloaded successfully.")
        except Exception as e:
            print(f"Error downloading VADER lexicon: {e}")
            print("\nYou can try:")
            print("1. Check your internet connection")
            print("2. Download manually: python -m nltk.downloader vader_lexicon")
            print("3. Check NLTK data path")
            sys.exit(1)

def get_analyzer():
    """
    Get or initialize the sentiment analyzer.
    
    Returns:
        SentimentIntensityAnalyzer instance
    """
    global _sia
    if _sia is None:
        _ensure_vader_lexicon()
    return _sia

def analyze_statement(text: str) -> Dict:
    """
    Analyze a single text statement with VADER.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with sentiment scores and label
        
    Example:
        >>> analyze_statement("I love this!")
        {
            "text": "I love this!",
            "compound": 0.6369,
            "neg": 0.0,
            "neu": 0.323,
            "pos": 0.677,
            "label": "Positive"
        }
    """
    if not text or not text.strip():
        return {
            "text": text,
            "compound": 0.0,
            "neg": 0.0,
            "neu": 1.0,
            "pos": 0.0,
            "label": "Neutral"
        }
    
    sia = get_analyzer()
    scores = sia.polarity_scores(text)
    compound = scores["compound"]
    label = label_from_compound(compound)
    
    return {
        "text": text,
        "compound": compound,
        "neg": scores["neg"],
        "neu": scores["neu"],
        "pos": scores["pos"],
        "label": label
    }

def label_from_compound(compound: float, 
                       pos_thresh: float = POSITIVE_THRESHOLD,
                       neg_thresh: float = NEGATIVE_THRESHOLD) -> str:
    """
    Map VADER compound score to label.
    
    Args:
        compound: VADER compound score (-1 to 1)
        pos_thresh: Threshold for positive sentiment (default: 0.05)
        neg_thresh: Threshold for negative sentiment (default: -0.05)
        
    Returns:
        "Positive", "Negative", or "Neutral"
    """
    if compound >= pos_thresh:
        return "Positive"
    elif compound <= neg_thresh:
        return "Negative"
    else:
        return "Neutral"

def conversation_level_sentiment(user_messages: List[str], 
                                system_messages: Optional[List[str]] = None) -> Dict:
    """
    Compute overall conversation sentiment based on user messages only.
    Uses weighted average based on message length.
    
    Args:
        user_messages: List of user message texts
        system_messages: Optional list of system messages (not used in calculation)
        
    Returns:
        Dictionary with overall sentiment analysis
        
    Example:
        >>> conversation_level_sentiment(["I love it", "I hate it"])
        {
            "compound": -0.1,
            "label": "Neutral",
            "details": [...],
            "message_count": 2
        }
    """
    # Note: system_messages parameter is kept for backward compatibility
    # but is not used in calculation as per assignment requirements
    
    if not user_messages:
        return {
            "compound": 0.0,
            "label": "Neutral",
            "details": [],
            "message_count": 0
        }
    
    details = []
    total_weight = 0.0
    weighted_sum = 0.0
    
    for text in user_messages:
        info = analyze_statement(text)
        
        # Weight by message length (word count) but with diminishing returns
        # Use log(length + 1) to avoid over-weighting long messages
        word_count = len(text.split())
        weight = max(1, int(word_count ** 0.5))  # Square root scaling
        
        weighted_sum += info["compound"] * weight
        total_weight += weight
        details.append({
            "text": text,
            "compound": info["compound"],
            "label": info["label"],
            "weight": weight
        })
    
    avg_compound = weighted_sum / total_weight if total_weight else 0.0
    overall_label = label_from_compound(avg_compound)
    
    return {
        "compound": avg_compound,
        "label": overall_label,
        "details": details,
        "message_count": len(user_messages),
        "weighted_average": True
    }

def sentiment_trend(user_messages: List[str], window: int = 2) -> List[Tuple[int, str, float]]:
    """
    Analyze sentiment trend across conversation with moving average.
    
    Args:
        user_messages: List of user message texts
        window: Size of moving window for averaging (default: 2)
        
    Returns:
        List of tuples (index, label, average_compound)
        
    Example:
        >>> sentiment_trend(["Good", "Bad", "Great"], window=2)
        [(0, 'Positive', 0.5), (1, 'Neutral', 0.0), (2, 'Positive', 0.4)]
    """
    if not user_messages:
        return []
    
    # Calculate compound scores for all messages
    compounds = []
    for msg in user_messages:
        info = analyze_statement(msg)
        compounds.append(info["compound"])
    
    trend = []
    n = len(compounds)
    
    for i in range(n):
        # Calculate moving average
        start = max(0, i - window + 1)
        window_vals = compounds[start:i + 1]
        avg = sum(window_vals) / len(window_vals)
        
        # Get label for the average
        label = label_from_compound(avg)
        
        trend.append((i, label, avg))
    
    return trend

def get_sentiment_statistics(user_messages: List[str]) -> Dict:
    """
    Get detailed sentiment statistics for conversation.
    
    Args:
        user_messages: List of user message texts
        
    Returns:
        Dictionary with sentiment statistics
    """
    if not user_messages:
        return {
            "total_messages": 0,
            "sentiment_counts": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "percentages": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "average_compound": 0.0,
            "compound_std": 0.0
        }
    
    analyses = [analyze_statement(msg) for msg in user_messages]
    compounds = [a["compound"] for a in analyses]
    labels = [a["label"] for a in analyses]
    
    # Count sentiments
    sentiment_counts = {
        "Positive": labels.count("Positive"),
        "Negative": labels.count("Negative"),
        "Neutral": labels.count("Neutral")
    }
    
    # Calculate percentages
    total = len(user_messages)
    percentages = {
        key: (count / total * 100) for key, count in sentiment_counts.items()
    }
    
    # Calculate average and standard deviation
    avg_compound = sum(compounds) / total if total else 0.0
    
    if total > 1:
        variance = sum((c - avg_compound) ** 2 for c in compounds) / (total - 1)
        std_dev = variance ** 0.5
    else:
        std_dev = 0.0
    
    return {
        "total_messages": total,
        "sentiment_counts": sentiment_counts,
        "percentages": percentages,
        "average_compound": avg_compound,
        "compound_std": std_dev,
        "min_compound": min(compounds) if compounds else 0.0,
        "max_compound": max(compounds) if compounds else 0.0
    }

def detect_mood_shifts(user_messages: List[str], min_change: float = 0.3) -> List[Dict]:
    """
    Detect significant mood shifts in conversation.
    
    Args:
        user_messages: List of user message texts
        min_change: Minimum compound score change to consider as a shift
        
    Returns:
        List of dictionaries describing mood shifts
    """
    if len(user_messages) < 2:
        return []
    
    analyses = [analyze_statement(msg) for msg in user_messages]
    shifts = []
    
    for i in range(1, len(analyses)):
        prev = analyses[i - 1]
        curr = analyses[i]
        
        # Check if there's a significant change
        change = abs(curr["compound"] - prev["compound"])
        
        if change >= min_change or prev["label"] != curr["label"]:
            shifts.append({
                "message_index": i + 1,  # 1-based indexing
                "from_message": prev["text"],
                "to_message": curr["text"],
                "from_label": prev["label"],
                "to_label": curr["label"],
                "from_compound": prev["compound"],
                "to_compound": curr["compound"],
                "change_magnitude": change,
                "description": f"Mood shifted from {prev['label']} to {curr['label']}"
            })
    
    return shifts
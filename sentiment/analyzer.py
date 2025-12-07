# sentiment/analyzer.py
from typing import List, Dict, Tuple
import math

# NLTK VADER
import nltk
nltk.data.path.append("/Users/prachi/nltk_data")
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure required data is downloaded
try:
    _ = nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()

def analyze_statement(text: str) -> Dict:
    """
    Analyze a single text statement with VADER.
    Returns dict with compound, pos/neu/neg scores and label.
    """
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

def label_from_compound(compound: float, pos_thresh: float = 0.05, neg_thresh: float = -0.05) -> str:
    """
    Map VADER compound score to label.
    Default thresholds as recommended by VADER: >=0.05 -> positive, <=-0.05 -> negative, else neutral.
    """
    if compound >= pos_thresh:
        return "Positive"
    elif compound <= neg_thresh:
        return "Negative"
    else:
        return "Neutral"

def conversation_level_sentiment(user_messages: List[str], system_messages: List[str]=None) -> Dict:
    """
    Compute an overall conversation sentiment based on all user messages (and optionally system messages).
    Strategy:
      - Compute VADER compound for each message
      - Weight each message's compound by its token length (approx by word count) to reduce small-message bias
      - Compute weighted average compound, then map to label
    Returns dict with overall compound, label and breakdown.
    """
    if system_messages is None:
        system_messages = []
    all_msgs = user_messages + system_messages

    if not all_msgs:
        return {"compound": 0.0, "label": "Neutral", "details": []}

    details = []
    total_weight = 0.0
    weighted_sum = 0.0

    for t in all_msgs:
        info = analyze_statement(t)
        weight = max(1, len(t.split()))  # at least 1, approx word count
        weighted_sum += info["compound"] * weight
        total_weight += weight
        details.append({"text": t, "compound": info["compound"], "weight": weight, "label": info["label"]})

    avg_compound = weighted_sum / total_weight if total_weight else 0.0
    overall_label = label_from_compound(avg_compound)
    return {"compound": avg_compound, "label": overall_label, "details": details}

def sentiment_trend(user_messages: List[str], window:int=2) -> List[Tuple[int, str, float]]:
    """
    Produce a simple trend summary across user messages:
      - Compute compound per message
      - Optionally compute a moving average (window)
    Returns list of tuples: (index, label, compound)
    """
    compounds = [sia.polarity_scores(m)["compound"] for m in user_messages]
    trend = []
    n = len(compounds)
    for i in range(n):
        start = max(0, i - window + 1)
        window_vals = compounds[start:i+1]
        avg = sum(window_vals) / len(window_vals)
        label = label_from_compound(avg)
        trend.append((i, label, avg))
    return trend

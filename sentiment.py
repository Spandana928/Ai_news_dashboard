from textblob import TextBlob

def get_sentiment(text):
    if not text:
        return "Neutral"
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.01:      # More sensitive
        return "Positive"
    elif polarity < -0.01:
        return "Negative"
    else:
        return "Neutral"




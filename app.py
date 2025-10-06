from flask import Flask, render_template, request, send_file
from news_fetcher import fetch_news
from sentiment import get_sentiment
from generate_pdf import generate_pdf
import plotly.graph_objs as go
import plotly.io as pio
import openai
import threading

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your valid key


# -----------------------------
# Helper: Summarize text using OpenAI
# -----------------------------
def summarize_text(text):
    """Generate AI summary using OpenAI GPT."""
    if not text:
        return "No content available."
    try:
        prompt = f"Summarize this news article in 2-3 sentences:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary if summary else text
    except Exception as e:
        print("OpenAI API error:", e)
        return text


# -----------------------------
# Background thread for AI summaries
# -----------------------------
def fetch_ai_summaries(news_list):
    """Fetch AI summaries and sentiments in background."""
    for n in news_list:
        n['summary'] = summarize_text(n['description'])
        n['sentiment'] = get_sentiment(n['summary'])


# -----------------------------
# Home Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    news_data = None
    topic = ""
    chart_div = None

    if request.method == "POST":
        topic = request.form.get("topic")
        news_data = fetch_news(topic=topic, page_size=10)

        if not news_data:
            return render_template("index.html", news=[], topic=topic, chart_div=None)

        # Assign initial summaries & sentiments
        sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
        for n in news_data:
            n['summary'] = n['description']
            n['sentiment'] = get_sentiment(n['summary'])
            sentiments[n['sentiment']] += 1

        print("Sentiment counts (initial):", sentiments)  # Debug

        # Start background thread for AI summaries (non-blocking)
        thread = threading.Thread(target=fetch_ai_summaries, args=(news_data,))
        thread.start()

        # Generate sentiment chart (only if data exists)
        # Generate sentiment chart (only if data exists)
        if any(sentiments.values()):
            fig = go.Figure([
                go.Bar(
                    x=list(sentiments.keys()),  # Horizontal categories
                    y=list(sentiments.values()),  # Vertical heights
                    marker=dict(color=['green', 'red', 'gray']),
                    width=0.5  # adjust bar width for a nicer look
                )
            ])
            fig.update_layout(
                title_text='Sentiment Analysis',
                xaxis_title='Sentiment',
                yaxis_title='Count',
                plot_bgcolor='white',
                bargap=0.3,
                height=400,
                width=500,
                font=dict(size=14)
            )
            chart_div = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
        else:
            chart_div = "<p>No sentiment data available.</p>"


    return render_template("index.html", news=news_data, topic=topic, chart_div=chart_div)


# -----------------------------
# PDF Download Route
# -----------------------------
@app.route("/download_pdf/<topic>")
def download_pdf(topic):
    news_data = fetch_news(topic=topic, page_size=10)
    for n in news_data:
        n['summary'] = summarize_text(n['description'])
        n['sentiment'] = get_sentiment(n['summary'])
    pdf_file = generate_pdf(news_data, topic)
    return send_file(pdf_file, as_attachment=True)


# -----------------------------
# Run Flask app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)






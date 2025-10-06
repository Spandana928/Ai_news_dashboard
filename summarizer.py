import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def summarize_text(text):
    if not text:
        return "No content to summarize."
    prompt = f"Summarize the following news article in 2-3 sentences:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']


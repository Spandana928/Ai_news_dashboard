# AI News Dashboard

A Flask-based web dashboard that fetches the latest AI news, analyzes trends, and displays visual charts.

---

## Features

- Display latest AI news headlines.
- Interactive topic selection.
- Visual charts of trends using Plotly.
- Responsive UI with dynamic data updates.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Data Visualization:** Plotly
- **Deployment:** Render.com
- **Package Management:** pip

---

## Project Structure

project-root/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # Main HTML template
├── static/
│ ├── css/ # CSS files
│ ├── js/ # JavaScript files
│ └── images/ # Images and icons
└── README.md



---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Spandana928/ai-news-dashboard.git
cd ai-news-dashboard
Install dependencies

pip install -r requirements.txt


Run locally

flask run
Deployment

This app is deployed on Render

Make sure all templates are in the templates/ folder and static assets are in static/.

The requirements.txt should include gunicorn for production.

Example Render start command:

gunicorn app:app

live link: https://ai-news-dashboard.onrender.com/

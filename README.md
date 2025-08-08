Project Title: News Summarizer and Sentiment Analyzer Web App
Description:
Developed a Flask-based web application that allows users to search, summarize, and analyze the sentiment of news articles. Integrated multiple NLP tools to deliver concise insights from raw news data and supported multilingual summarization using translation APIs.


working model : https://ainewsassist.onrender.com/


Key Features:

🔍 News Search & Display: Integrated with NewsAPI to fetch real-time articles based on user-input keywords.

📰 Text & URL Summarization: Extracted and summarized key points from user-submitted text or online news URLs using the LexRank algorithm (Sumy) and newspaper3k.

🌐 Multilingual Support: Enabled summary translation to various languages using Google Translate API.

😊 Sentiment Analysis: Performed polarity and subjectivity evaluation using TextBlob for insights into article tone.

🔧 Frontend Integration: Used Flask routes and render_template for rendering HTML templates (index.html, summary.html, url.html, etc.).

🔐 CORS Configuration: Enabled Cross-Origin Resource Sharing (CORS) to ensure smooth frontend-backend communication.

☁️ RESTful API Design: Exposed endpoints for summary generation, news search, and analysis in a structured JSON format.

Tech Stack:

Backend: Python, Flask

NLP Libraries: TextBlob, newspaper3k, Sumy (LexRank)

APIs: NewsAPI, Google Translate

Others: CORS, REST, HTML templates (Jinja2)


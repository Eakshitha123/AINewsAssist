from flask import Flask, request, jsonify, render_template
from newspaper import Article
from textblob import TextBlob
from flask_cors import CORS
import requests
from googletrans import Translator
from newsapi import NewsApiClient
from dotenv import load_dotenv
from summa import summarizer
import os

app = Flask(__name__)
load_dotenv()
CORS(app)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/url')
def url_summarize():
    return render_template('url.html')

@app.route('/search_news', methods=['POST'])
def search_news():
    data = request.get_json()
    keyword = data.get('keyword', '')

    if not keyword or keyword.strip() == ' ':
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        corrected_text = str(TextBlob(keyword).correct())
        results = newsapi.get_everything(q=corrected_text, language='en', page_size=10)

        articles = []
        for article in results['articles']:
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'image': article['urlToImage']
            })

        return jsonify(articles)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/default_news')
def default_news():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=us&'
           f'apiKey={NEWS_API_KEY}')
    try:
        response = requests.get(url)
        data = response.json()

        articles = []
        for item in data.get('articles', []):
            articles.append({
                'title': item.get('title'),
                'description': item.get('description'),
                'url': item.get('url'),
                'image': item.get('urlToImage')
            })

        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get('text')

    if not text or len(text.strip()) == 0:
        return jsonify({"error": "Text is empty."}), 400

    try:
        # Summarize text with summa
        summary = summarizer.summarize(text, ratio = 0.3)
        if not summary:
            summary = text  # fallback

        # Sentiment analysis on summary
        blob = TextBlob(summary)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        sentiment = "😊 Positive" if polarity > 0 else "😐 Neutral" if polarity == 0 else "😠 Negative"

        return jsonify({
            "summary": summary,
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarize_url', methods=['POST'])
def summarize_url():
    data = request.json
    url = data.get('url')
    lang = data.get('language', 'en')  # default to English if not provided

    try:
        article = Article(url)
        article.download()
        article.parse()

        article_text = article.text
        summary = summarizer.summarize(article_text, words=100)
        if not summary:
            summary = article_text  # fallback

        # Translate summary to requested language
        translator = Translator()
        translated_summary = summary
        translated_title = article.title
        if lang != 'en':  # translate only if language is not English
            translated = translator.translate(summary, dest=lang)
            translated_summary = translated.text
            translated_title = translator.translate(article.title,dest=lang).text

        
        authors = article.authors
        top_image = article.top_image

        # Sentiment analysis on original summary (English)
        blob = TextBlob(summary)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        sentiment = "😊 Positive" if polarity > 0 else "😐 Neutral" if polarity == 0 else "😠 Negative"

        return jsonify({
            "title": translated_title,
            "authors": authors,
            "top_image": top_image,
            "summary": translated_summary,   # translated summary
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)

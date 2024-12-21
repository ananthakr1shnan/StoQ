import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from data import (
    get_top_thirteen_f,
    get_earnings_report,
    get_all_filings,
    get_benzinga_news,
    get_yahoo_news
)
import hnswlib
from groq import Groq
import datetime as dt
import yfinance as yf
from functools import lru_cache
from dotenv import load_dotenv
import os
import cohere
import openai
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Union
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
from algorithm import write_algorithm

# Load environment variables
load_dotenv()

# Initialize API clients
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SAMBA_API = os.getenv("SAMBA_API")

co = cohere.Client(COHERE_API_KEY)
samba = openai.OpenAI(api_key=SAMBA_API, base_url="https://api.sambanova.ai/v1")
groq_client = Groq(api_key=GROQ_API_KEY)

# Global state management
class AppState:
    def __init__(self):
        self.embedded_stocks = set()
        self.vectorstore = None
        self.initialized = False

state = AppState()

class Vectorstore:
    def __init__(self, documents):
        self.index = hnswlib.Index(space="cosine", dim=768)
        self.documents = documents
        self.index.init_index(max_elements=len(documents), ef_construction=200, M=16)

    def add_documents(self, documents):
        for doc in documents:
            self.documents.append(doc)
            vector = self.embed(doc["text"])
            self.index.add_items(vector, [len(self.documents) - 1])

    def retrieve(self, query):
        query_vector = self.embed(query)
        indices, distances = self.index.knn_query(query_vector, k=5)
        return [self.documents[i] for i in indices[0]]

    @staticmethod
    def embed(text):
        return co.embed(model="embed-english-light-v2.0", texts=[text]).embeddings[0]

def initialize_vectorstore():
    """Initialize the vectorstore with base documents."""
    print("Initializing vectorstore...")
    state.vectorstore = Vectorstore([{"title": "investopedia", "url": "https://www.investopedia.com/"}])
    state.initialized = True

def ensure_stock_embedded(ticker: str) -> None:
    """Ensure a stock's data is embedded in the vectorstore."""
    if not state.initialized:
        initialize_vectorstore()
    
    if ticker not in state.embedded_stocks:
        print(f"Embedding documents for {ticker}...")
        try:
            raw_documents = []
            raw_documents.extend(get_all_filings(ticker))
            raw_documents.extend(get_benzinga_news([ticker]))
            raw_documents.extend(get_yahoo_news(ticker))

            state.vectorstore.add_documents(raw_documents)
            state.embedded_stocks.add(ticker)
            print(f"Successfully embedded documents for {ticker}")
        except Exception as e:
            print(f"Error embedding documents for {ticker}: {e}")
    else:
        print(f"Documents for {ticker} are already embedded.")

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Initialize state before first request
    with app.app_context():
        if not state.initialized:
            initialize_vectorstore()
            ensure_stock_embedded("AAPL")

    @app.route('/top_thirteen_f', methods=['GET', 'POST'])
    @lru_cache(maxsize=32)
    def top_thirteen_f():
        holdings = get_top_thirteen_f()
        return jsonify(holdings)

    @app.route('/earnings_report', methods=['GET', 'POST'])
    @lru_cache(maxsize=32)
    def earnings_report():
        ticker = request.args.get('ticker')
        year = int(request.args.get('year'))
        quarter = int(request.args.get('quarter'))
        financials = get_earnings_report(ticker, year, quarter)
        return jsonify(financials)

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        message = data.get('message')
        chat_history = data.get('chat_history', [])
        
        if not message:
            return jsonify({"error": "Message is required"}), 400

        try:
            ticker_response = co.chat(
                model="command-r-plus",
                preamble="Return only the ticker (2-4 characters) for the company mentioned",
                message=message,
                connectors=[{"id": "web-search"}]
            )
            ticker = ticker_response.text.strip().upper()

            ensure_stock_embedded(ticker)

            search_response = co.chat(
                message=message,
                preamble="Generate search queries for the stock analysis",
                model="command-r-plus",
                search_queries_only=True,
                chat_history=chat_history
            )

            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant specializing in stock analysis and financial information.",
                },
                *chat_history,
                {
                    "role": "user",
                    "content": message,
                }
            ]

            if search_response.search_queries:
                documents = []
                for query in search_response.search_queries:
                    documents.extend(state.vectorstore.retrieve(query.text))
                
                context = "\n".join(doc["text"] for doc in documents)
                messages[0]["content"] += f"\nContext: {context}"

            completion = groq_client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=4096
            )

            return jsonify({
                "response": completion.choices[0].message.content,
                "citations": getattr(completion, 'citations', None)
            })

        except Exception as e:
            print(f"Error in chat processing: {e}")
            return jsonify({"error": str(e)}), 500

    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("Starting the server...")
    app.run(debug=True, port=8081, use_reloader=False)
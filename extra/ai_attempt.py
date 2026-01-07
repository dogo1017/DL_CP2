import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression # A good starting model for text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import wikipedia
from word2number import w2n
import requests
from bs4 import BeautifulSoup

# --- CLASSIFICATION SETUP AND TRAINING ---

def train_classifier():
    # Load your training data from the CSV you are building
    # Make sure 'prompts.csv' is in the same directory as this script
    try:
        df = pd.read_csv('prompts.csv')
    except FileNotFoundError:
        print("Error: prompts.csv not found. Please create your spreadsheet first.")
        # Create a dummy dataframe for demonstration if file missing
        df = pd.DataFrame({
            'prompt_text': ["What is 5 plus 5?", "Summarize the Wikipedia page for AI", "Write a basic Python function", "Summarize this website: google.com"],
            'category': ["math", "summary", "code", "summary"]
        })

    # Split data (not strictly necessary with tiny data, but good practice)
    X_train, X_test, y_train, y_test = train_test_split(df['prompt_text'], df['category'], test_size=0.2, random_state=42)

    # Convert text data into numerical features (vectorization)
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8)
    X_train_vec = vectorizer.fit_transform(X_train)
    
    # Train the classification model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    # Optional: Check model accuracy
    # predictions = model.predict(vectorizer.transform(X_test))
    # print(f"Model Accuracy: {accuracy_score(y_test, predictions)*100:.2f}%")

    return model, vectorizer

# --- FUNCTIONALITY (MATH, SUMMARY, CODE) ---

def handle_wikipedia_summary(search_term, sentences_inp=3):
    # (Your existing Wikipedia code moved into a function)
    try:
        search_results = wikipedia.search(search_term)
        if not search_results: return "Could not find a matching page for the search term."
        page_summary = wikipedia.summary(search_results[0], sentences=sentences_inp)
        return f"\nSummary of {search_results[0]}:\n{page_summary}"
    except Exception as e:
        return f"An error occurred during summary retrieval: {e}"

def handle_url_summary(url, sentences_inp=3):
    # Added function to handle website summaries
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Simple extraction: get all paragraph text
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        full_text = ' '.join(paragraphs)
        # In a real app, you'd feed full_text into another summarization AI
        return f"Summary of {url}: (Basic extraction)\n{full_text[:300]}..."
    except requests.exceptions.RequestException as e:
        return f"Could not retrieve URL: {e}"


def handle_math_request(text):
    # This is complex to parse natural language math, but here's a start
    return f"Math logic needed for: '{text}'. (Requires an expression parser)"

def handle_code_request(text):
    # This requires an LLM or predefined templates
    return f"Code logic needed for: '{text}'. (Requires AI code generation)"


# --- MAIN EXECUTION LOGIC ---

if __name__ == "__main__":
    # 1. Train the classifier once when the script starts
    print("Training the intent classifier...")
    classifier_model, vectorizer = train_classifier()
    print("Classifier ready.")
    
    while True:
        user_input = input("\nEnter your request (math, summary, or code): ")
        if user_input.lower() == 'exit':
            break
        
        # 2. Use the trained model to predict the category
        input_vectorized = vectorizer.transform([user_input])
        prediction = classifier_model.predict(input_vectorized)[0]
        
        print(f"Detected Category: --> {prediction} <--")

        # 3. Route the request to the appropriate function
        if prediction == 'summary':
            # Need basic logic to figure out subject/URL
            if "http" in user_input or "www" in user_input:
                 # Simple URL extraction (needs robust parsing later)
                 url = [word for word in user_input.split() if "http" in word or "www" in word][0]
                 result = handle_url_summary(url)
            else:
                # Basic subject extraction
                subject = user_input.replace("summarize", "").replace("summary of", "").strip()
                result = handle_wikipedia_summary(subject)
            print(result)

        elif prediction == 'math':
            print(handle_math_request(user_input))
        
        elif prediction == 'code':
            print(handle_code_request(user_input))
        
        else:
            print("Could not determine intent.")
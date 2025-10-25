import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import re
import os

# Download necessary NLTK data files robustly
def ensure_nltk_resource(resource_name, download_name=None):
    try:
        nltk.data.find(resource_name)
    except LookupError:
        nltk.download(download_name if download_name else resource_name.split('/')[-1])

ensure_nltk_resource('corpora/stopwords', 'stopwords')
ensure_nltk_resource('corpora/wordnet', 'wordnet')
ensure_nltk_resource('tokenizers/punkt', 'punkt')
ensure_nltk_resource('tokenizers/punkt_tab', 'punkt_tab')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Global variable to hold the pre-processed PDF text
_pdf_content = ""

def set_pdf_content(text):
    """Sets the global PDF content for answering questions."""
    global _pdf_content
    _pdf_content = text

def is_pdf_active():
    """Checks if there is a PDF loaded and ready for questions."""
    return len(_pdf_content) > 0

def preprocess_text(text):
    """Tokenizes, removes stopwords, and lemmatizes the input text."""
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    tokens = word_tokenize(text.lower())
    # Remove stopwords and lemmatize
    filtered_tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(filtered_tokens)

def answer_question_from_pdf(pdf_text, question):
    """
    Answers a question based on the content of a PDF.
    
    This function uses a simple method to find the most relevant sentence
    in the PDF content by comparing the similarity of the question and each sentence.
    """
    if not pdf_text:
        return "I haven't read any PDF content yet. Please read a PDF first."

    # Split the PDF content into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', pdf_text)
    
    # Preprocess the question and each sentence
    processed_sentences = [preprocess_text(s) for s in sentences]
    processed_question = preprocess_text(question)

    if not processed_question:
        return "Please ask a question with some keywords I can search for."

    # Combine the question and sentences for TF-IDF vectorization
    all_texts = [processed_question] + processed_sentences
    
    # Vectorize the text data
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity between the question and each sentence
    question_vector = tfidf_matrix[0:1]
    sentence_vectors = tfidf_matrix[1:]
    cosine_similarities = cosine_similarity(question_vector, sentence_vectors).flatten()

    # Find the index of the most similar sentence
    most_similar_index = cosine_similarities.argmax()

    # Get the most relevant sentence
    best_sentence = sentences[most_similar_index]
    
    # Check if the similarity is very low, which might mean the answer isn't in the document
    if cosine_similarities[most_similar_index] < 0.1:
        return "I am sorry, but I couldn't find a relevant answer in the document."
    
    return best_sentence
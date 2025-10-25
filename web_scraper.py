import requests
from bs4 import BeautifulSoup

def get_text_from_url(url):
    """
    Fetches the content from a URL and extracts the text from all <p> tags.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraph tags and join their text
        paragraphs = soup.find_all('p')
        text_content = ' '.join([p.get_text() for p in paragraphs])
        
        # If no paragraphs are found, get all text
        if not text_content.strip():
            text_content = soup.get_text(separator=' ', strip=True)

        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while scraping the URL: {e}")
        return None
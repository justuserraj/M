import pyttsx3
import PyPDF2
import newspaper
import os

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def read_pdf_aloud(file_path):
    """Reads the content of a PDF file aloud."""
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            speak("Sorry, I could not find that file.")
            print(f"Error: File not found at {file_path}")
            return

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            speak(f"Found {num_pages} pages. Starting to read now.")
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    speak(f"Reading page {page_num + 1}:")
                    speak(text)
                else:
                    speak(f"Page {page_num + 1} is empty or unreadable.")
        
        speak("Finished reading the PDF.")

    except Exception as e:
        speak("Sorry, an error occurred while trying to read the PDF.")
        print(f"Error reading PDF: {e}")

def read_article_aloud(url):
    """Reads the content of a web article aloud."""
    try:
        speak("Downloading and parsing the article now.")
        article = newspaper.Article(url)
        article.download()
        article.parse()
        
        if article.text:
            speak(f"Reading article titled: {article.title}.")
            speak(article.text)
            speak("Finished reading the article.")
        else:
            speak("Sorry, I couldn't find any readable text in that article.")

    except newspaper.article.ArticleException as e:
        speak("Sorry, I couldn't access that URL. Please check the link.")
        print(f"Error in article reader: {e}")
    except Exception as e:
        speak("Sorry, an error occurred while trying to read the article.")
        print(f"Error reading article: {e}")
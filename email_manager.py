import pyttsx3
import smtplib
import ssl

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def send_email(receiver_email, subject, body):
    """Sends an email to a specified recipient."""

    SENDER_EMAIL = "justuserraj@gmail.com"  # <-- REPLACE THIS
    APP_PASSWORD = "aukv vcre wffn rlos"  # <-- REPLACE THIS

    # Set up the secure connection
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            
            message = f"Subject: {subject}\n\n{body}"
            
            # Send the email
            server.sendmail(SENDER_EMAIL, receiver_email, message)
        
        speak("Email sent successfully!")
        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        speak("Sorry, I couldn't send the email. Please check your email and app password.")
        print("SMTPAuthenticationError: Incorrect email or app password.")
    except Exception as e:
        speak("Sorry, I'm unable to send the email at this time.")
        print(f"Error sending email: {e}")
import os
import speech_recognition as sr
from gtts import gTTS
import tempfile
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def openai_ai_assistant(input_text):
    """
    Get AI response using OpenAI's chat model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use other models as well
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ],
            temperature=0
        )
        # Accessing the response using attributes in OpenAI 1.9.0
        response_message = response.choices[0].message.content
        return response_message
    except Exception as e:
        return "An error occurred: " + str(e)



def speak(text):
    """
    Use Google Text-to-Speech to speak the response.
    """
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts = gTTS(text=text, lang='en')
        tts.save(fp.name)
        os.system(f"afplay {fp.name}")

def recognize_speech_from_mic(recognizer, microphone):
    """
    Transcribe speech from recorded from `microphone`.
    """
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        return "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        return "Unable to recognize speech"

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Welcome to the AI Assistant! Say 'goodbye' to exit.")
    speak("Welcome Daylin, How can I assist you today?")
    
    while True:
        print("Listening...")
        user_input = recognize_speech_from_mic(recognizer, microphone)
        print("You said:", user_input)

        if user_input.lower() == "goodbye":
            speak("Goodbye! It was nice talking to you.")
            break

        response = openai_ai_assistant(user_input)
        print("AI Assistant:", response)
        speak(response)

if __name__ == "__main__":
    main()

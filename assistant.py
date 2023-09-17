import pyttsx3
import webbrowser
import speech_recognition as sr
import datetime
import wikipediaapi
import pyjokes


Assistant = pyttsx3.init()
voices = Assistant.getProperty("voices")
Assistant.setProperty("voice", voices[0].id)

def Speak(audio):
    print("   ")
    Assistant.say(audio)
    Assistant.runAndWait()

def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hearing....")
        command.pause_threshold = 0.5  # Reduce the pause threshold for faster response
        audio = command.listen(source)

        try:
            print("Recognizing....")
            query = command.recognize_google(audio, language="en-in")
            print(f"command : {query}")
        except sr.UnknownValueError:
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return "None"
        return query.lower()

def search_wikipedia(query):
    # Initialize the Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia("en")
    
    # Use the API to search for the query
    page = wiki_wiki.page(query)
    
    # Check if the page exists
    if page.exists():
        content = page.summary
        Speak(content)
    else:
        Speak(f"Sorry, I couldn't find information about {query} on Wikipedia.")

def TaskExe():
    while True:
        query = takecommand()

        if "hello" in query:
            Speak("Hello! How can I assist you today?")
        elif 'who are you' in query:
            Speak("I am your virtual assistant. What can I do for you?")
            
        elif 'say hi to' in query:
            query = query.replace("say hi to", "")
            Speak(f"hello {query}, how are you? ")
            
        elif 'weather' in query:
            Speak("I'm sorry, I don't have access to real-time weather data.")
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            Speak(joke)
        elif 'date' in query:
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
            Speak(f"Today's date is {current_date}")
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            Speak(f"The current time is {current_time}")
        elif 'search for' in query:
            query = query.replace("search for", "").strip()
            search_wikipedia(query)
        elif 'riddle' in query:
            Speak("Sure, here's a riddle: What comes once in a minute, twice in a moment, but never in a thousand years?")
        elif 'youtube search' in query:
            query = query.replace("youtube search", "")
            web = 'https://www.youtube.com/results?search_query=' + query
            webbrowser.open(web)
            Speak('Done sir')

        elif 'google search' in query:
            query = query.replace("google search", "")
            web = 'https://www.google.com/search?q=' + query
            webbrowser.open(web)
            Speak('Done sir')

        elif 'turn off' in query or 'bye' in query:
            Speak("Ok Sir, you can call me anytime!")
            break
        else:
            Speak("I'm sorry, I didn't understand your query. How can I assist you?")

TaskExe()

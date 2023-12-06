import pyttsx3
import webbrowser
import speech_recognition as sr
import datetime
import google.generativeai as palm
import smtplib


palm.configure(api_key='     *****Add your key heare*******      ')
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

Assistant = pyttsx3.init()
voices = Assistant.getProperty("voices")
Assistant.setProperty("voice", voices[0].id)

def Speak(audio):
    print("   ")
    Assistant.say(audio)
    Assistant.runAndWait()
    
def sendEmail(to, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("teamgangamitra@gmail.com", "pvyy eheg jcbd dbku")
    body = f"Subject: {subject}\n\n{message}"
    server.sendmail("teamgangamitra@gmail.com", to, body)
    server.quit()

def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hearing....")
        command.pause_threshold = 0.5 # Reduce the pause threshold for faster response
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
            
        elif 'date' in query:
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
            Speak(f"Today's date is {current_date}")
            
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            Speak(f"The current time is {current_time}")
        
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
            
        elif 'send email' in query or "send mail" in query:
            print("send E-mail to?")
            Speak("send E-mail? to")
            to = takecommand()
            if "01" in to:
             to = to.replace("01", "niwaneyash@gmail.com")
            print(to)
            print("What will be the subject of  Email?")
            Speak("What will be the subject of  Email?")
            subject = takecommand()
            print("what will be the message?")
            Speak("what will be the message?")
            message = takecommand()
            sendEmail(to, subject, message)
            print("email send successfully")
            Speak("email send successfully")
        
        elif 'turn off' in query or 'bye' in query:
            Speak("Ok Sir, you can call me anytime!")
            break
        
        else:
            prompt=query
            response = palm.chat(messages=prompt)
            response = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
                     
            max_output_tokens=100,
)
            Speak(response.result)
            print(response.result)     
TaskExe()

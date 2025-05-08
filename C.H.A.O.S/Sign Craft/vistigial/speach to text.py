import speech_recognition as sr
import pyttsx3

#recognizer init
r = sr.Recognizer()

def record_text():

    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                audio2 = r.listen(source2)

                mytext = r.recognize_google(audio2)
                print(mytext)

                return mytext

        except sr.RequestError as e:
            print("could not request results: {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

    return


def output_text(text):
    return

while(1):
    text = record_text()
    output_text(text)

    print('Wrote text')


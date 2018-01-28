import os
import re

import pyautogui
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from win10toast import ToastNotifier

toaster = ToastNotifier()

mixer.init()

toaster.show_toast("Python Speech Recognition",
                   "Script Starting", duration=3)

dirlist = os.listdir('.')  # Clear all old tts files
for f in dirlist:
    if not f.find('tts_file') == -1:
        os.remove(f)

i = 0


def tts(par1):
    global i
    sf = gTTS(text=par1, lang='en', slow=False)
    try:
        os.remove("tts_file" + str(i) + ".mp3")
    except WindowsError:
        pass
    sf.save("tts_file" + str(i) + ".mp3")
    mixer.music.load("tts_file" + str(i) + ".mp3")
    mixer.music.play()
    i += 1


# obtain audio from the microphone
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for speech")
        audio = r.listen(source)

    # recognize speech using Google
    try:
        speech = r.recognize_google(audio)
        if re.search(r"(exit|quit) (speech|jarvis)", speech.lower()) is not None:
            break
        elif re.search(r"(next|skip) (song|track)", speech.lower()) is not None:
            os.system('CLMControl spotify -nt')
            toaster.show_toast("Python Speech Recognition",
                               "Skipping song")
        elif re.search(r"(last|previous) (song|track)", speech.lower()) is not None:
            os.system('CLMControl spotify -pt')
            os.system('CLMControl spotify -pt')
            toaster.show_toast("Python Speech Recognition",
                               "Skipping song")
        elif re.search(r"(reset|restart) (song|track)", speech.lower()) is not None:
            os.system('CLMControl spotify -pt')
            toaster.show_toast("Python Speech Recognition",
                               "Skipping song")
        elif re.search(r"(pause|play) (song|music)", speech.lower()) is not None:
            os.system('CLMControl spotify -pp')
            toaster.show_toast("Python Speech Recognition",
                               "Pause Music")
        elif re.search(r"sleep (mode|computer)", speech.lower()) is not None:
            toaster.show_toast("Python Speech Recognition",
                               "Sleep Mode", duration=3)
            os.system('shutdown /h')
        elif re.search(r"(search (google|for)|google|look up)", speech.lower()) is not None:
            mo = re.search(r"(search (google|for)|google|look up)", speech.lower())
            query = speech.lower().replace(mo.group(0), "")
            os.startfile("http://www.google.com/search?q=" + query.replace(" ", "+"))
        elif re.search(r"(kill|exit|quit|close) (app|program|application)", speech.lower()) is not None:
            mo = re.search(r"(kill|exit|quit|close) (app|program|application)", speech.lower())
            query = speech.lower().replace(mo.group(0), "")
            os.system('taskkill /fi "WINDOWTITLE eq ' + query + '"')
        elif speech.lower() == "volume up":
            pyautogui.press("volumeup")
        elif speech.lower() == "volume down":
            pyautogui.press("volumedown")
        elif speech.lower() == "mute" or speech.lower() == "unmute":
            pyautogui.press("volumemute")
        else:
            tts("I'm sorry, I couldn't understand that")

        print("Speech Recognized: " + speech)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

toaster.show_toast("Python Speech Recognition",
                   "Script Exit", duration=3)

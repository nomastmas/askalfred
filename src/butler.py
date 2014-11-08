import re
from subprocess import call
# for processing google text to speech URL
from shlex import split
import sys
from actions import weather
from actions import switch
from os import path
#import facebook
#import directv
#import gracenote
#import camera
#import myemail
#import textmessage

# design note: alfred will ONLY process textual data, all sound recording/processing is done elsewhere
class Alfred:
        
    def __init__(self):
        "I am alfred"
        # constants
        self.__name = "Alfred"

        script_dir = path.dirname(path.realpath(__file__))
        audio_dir = "/".join(script_dir.split('/')[:-1]) + "/audio"

        self.okay_wav = audio_dir + "/okay.wav"
        self.repeat_wav = audio_dir + "/repeat.wav"


    def says(self,message):
        "Alfred's response to queries"
        if (re.search("okay", message)):
            command = split("/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols " + self.okay_wav)
        elif (re.search("repeat", message)):
            command = split("/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols " + self.repeat_wav)
        else: 
            command = split("/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols 'http://translate.google.com/translate_tts?tl=en&q=" + message + "'")
        call(command)
        print("alfred says: " + str(message))

    def is_summoned (self,message):
        "Alfred checks if he is summoned"
        if re.search(self.__name, message):
            return True
        else:
            return False

    def respond_to(self, message):
        "Alfred is summoned process command or record command"
        if re.search("weather|forecast", message):
            "handle weather here"
            weather.handler(message, self)
            return True
        elif re.search("on|off", message):
            "handle switch functions here"
            switch.handler(message,self)
            return True
        elif re.search("/cancel|nevermind/", message):
            return True

        print("did not handle anything")
        return False

if (__name__ == '__main__'):
    print("testing simple queries with Alfred")

    if (len(sys.argv) > 1):
        single_query = True
    else:
        single_query = False
    alfred = Alfred()
    while (1):
        try:
            if (single_query):
                query = sys.argv[1]
            else:
                query = raw_input("> ")
            
            alfred.respond_to(query)

            if (single_query):
                exit(0)
            
        except KeyboardInterrupt as e:
            print("ctrl+c caught, exiting gracefully like swan")
            exit(0)

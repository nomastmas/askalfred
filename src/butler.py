import re
from subprocess import call
# for processing google text to speech URL
from shlex import split
#import facebook
from actions import weather
from actions import switch
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


    def says(self,message):
        "Alfred's response to queries"
        command = split("/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols 'http://translate.google.com/translate_tts?tl=en&q=" + message + "'")
        call(command)
        print("alfred says: " + str(message))

    def is_summoned (self,message):
        "Alfred checks if he is summoned"
        if re.search(self.__name, message):
            return True
        else:
            return False

    def process_action(self, message):
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

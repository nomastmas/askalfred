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
from mic import Mic,NoParsableSpeech

# design note: alfred will ONLY process textual data, all sound recording/processing is done elsewhere
class Alfred:
        
    def __init__(self):
        "I am alfred"
        # constants
        self.__name = "Alfred"
        self.mic = Mic()


    def says(self,message):
        "Alfred's response to queries"
        command = split("/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols 'http://translate.google.com/translate_tts?tl=en&q=" + message + "'")
        call(command)
        print("alfred says: " + str(message))

    def listens(self, message):

        if (len(message) > 0 ):
            self.says("message")

        sample_width, sound_data = self.mic.record()
        self.mic.write_to_file(sample_width,sound_data)
        text = self.mic.get_text_from_google()

        return text

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
            weather.handle(message, self)
            return True
        elif re.search("on|off", message):
            "handle switch functions here"
            switch.handle(message,self)
            return True
        elif re.search("/cancel|nevermind/", message):
            return True

        print("did not handle anything")
        return False

from mic import Mic,NoParsableSpeech
from butler import Alfred

if __name__ == '__main__':
    print("my name is alfred")

    alfred = Alfred()
    mic = Mic()
    

    while 1:
        try:
            #TODO try to have it as
            # text = mic.record() 
            # where it records your voice, and returns plain text
            sample_width, sound_data = mic.record()
            mic.write_to_file(sample_width,sound_data)
            text = mic.get_text_from_google()

            # sample queries:
            # |Alfred| |lights on|
            # |Alfred lights on|
            print("|| " + text + " ||")
            if(not alfred.is_summoned(text)):
                continue
        
            #alfred.says("okay, hold on")
            alfred.respond_to(text)
        except NoParsableSpeech as e:
            print(e.value)
            alfred.says("please repeat")

from mic import Mic,NoParsableSpeech
from butler import Alfred

if __name__ == '__main__':
    print("my name is alfred")

    alfred = Alfred()
    mic = Mic()

    while 1:
        try:
            alfred.says("how can i help you?")

            # try to have it as
            # text = mic.record() 
            # where it records your voice, and returns plain text
            sample_width, sound_data = mic.record()
            mic.write_to_file(sample_width,sound_data)
            text = mic.get_text_from_google()

            print(text)
            if(alfred.is_summoned(text)):
                alfred.says("okay, hold on")
                while 1:
                    if (alfred.respond_to(text)):
                        break
                    else:
                        alfred.says("pardon me?")
                        sample_width, sound_data = mic.record()
                        mic.write_to_file(sample_width,sound_data)
                        text = mic.get_text_from_google()
                        print(text)


        except NoParsableSpeech as e:
            print(e.value)

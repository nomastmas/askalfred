from mic import Mic,NoParsableSpeech
from butler import Alfred

if __name__ == '__main__':
    print("my name is alfred")

    alfred = Alfred()
    mic = Mic()

    while 1:
        try:
            alfred.says("how can i help you?")

            sample_width, sound_data = mic.record()
            mic.write_to_file(sample_width,sound_data)
            text = mic.get_text_from_google()

            if(alfred.is_summoned(text)):
                print(text)
                while 1:
                    if (alfred.process_action(text)):
                        break
                    else:
                        alfred.says("pardon me?")
                        sample_width, sound_data = mic.record()
                        mic.write_to_file(sample_width,sound_data)
                        text = mic.get_text_from_google()
                        print(text)


        except NoParsableSpeech as e:
            print(e.value)

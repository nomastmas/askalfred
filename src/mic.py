# for data structure order
from os import remove
from sys import byteorder
from array import array
from struct import pack

# for audio creation/manipulation
import pyaudio
import wave
from pydub import AudioSegment

# for google speech to text
import urllib2
import json


class NoParsableSpeech(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Mic():

    def __init__(self):
        "i am the mic"
        # loud breathing can hit 2000 from about 6-7 feet away
        # the pauses between spoken words is about 1000 from about 6-7 feet away
        # spoken words always score over 2000, average around 5000 6-7 feet away

        # listening threshold denotes the min sound intensity to start recording
        self.listening_threshold    = 2000
        self.silence_threshold      = 3000
        self.rate                   = 16000
        # silence counter increases each time sound intensity dips below the silence threshold
        self.silence_counter        = 20
        self.chunk_size             = 1024
        self.format = pyaudio.paInt16

        #TODO have user set this path instead
        # file paths
        self.wav_path = '/home/pi/audio/speech.wav'
        self.flac_path = '/home/pi/audio/speech.flac'

        # google speech to text
        self.speech_url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        self.headers = {'Content-Type': 'audio/x-flac; rate=' + str(self.rate), 'User-Agent':'Mozilla/5.0'}

    def is_silent(self, snd_data):
        "checks if sound intensity is below threshold"
        return max(snd_data) < self.silence_threshold

    def is_active(self, snd_data):
        "checks if mic is recording"
        return max(snd_data) > self.silence_threshold

    def clean_up(self):
        # clean up any files generated
        remove(self.wav_path);
        remove(self.flac_path);

    def record(self):
        "records sound from the mic"
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=self.format, channels=1, rate=self.rate,
                            input=True, output=True,
                            frames_per_buffer=self.chunk_size)

            num_silent = 0
            snd_started = False
            record_started = False

            # 'h' specifies signed short int for array type
            r = array('h')

            print("listening for commands...")

            while 1:
                # little endian, signed short
                snd_data = array('h', stream.read(self.chunk_size))
                if byteorder == 'big':
                    snd_data.byteswap()

                # only start recording once sound is intense enough
                if not record_started:
                    if max(snd_data) > self.listening_threshold:
                        record_started = True
                    else:
                        continue;

                #TODO start recording once silence is broken
                r.extend(snd_data)

                silent = self.is_silent(snd_data)

                if silent and snd_started:
                    num_silent += 1
                    print("silence: " + str(num_silent))
                elif not silent and not snd_started:
                    snd_started = True
                    print("snd_started is true")
                elif self.is_active(snd_data):
                    num_silent = 0
                if snd_started and num_silent == self.silence_counter:
                    print("num_silent hit " + str(self.silence_counter) + ", abort")
                    break

            # wtf is sample_width for?
            sample_width = p.get_sample_size(self.format)
            stream.stop_stream()
            stream.close()
            p.terminate()

            return sample_width, r
        except KeyboardInterrupt as e:
            print("ctrl+c caught, exiting gracefully like swan")
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.clean_up()
            exit(0)

    def write_to_file(self, sample_width, data):
        "writes sound data to file"

        # '<' denotes little endian byte order
        # little endian because of cd format
        data = pack('<' + ('h' * len(data)), *data)

        print ("writing to wav file")
        wf = wave.open(self.wav_path, 'wb')

        try:
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)
            wf.setframerate(self.rate)
            wf.writeframes(data)
            wf.close()
        except KeyboardInterrupt as e:
            print("ctrl+c caught, exiting gracefully like swan")
            wf.close()
            self.clean_up()
            exit(0)

    def convert_wav_to_flac(self):
        print("converting wav to flac")
        speech = AudioSegment.from_wav(self.wav_path)
        speech.export(self.flac_path, format="flac")

    def get_text_from_google(self):
        print("getting text from google")
        try:
            self.convert_wav_to_flac()
            flac_file = open(self.flac_path, 'rb').read()

            # construct http request
            request = urllib2.Request(self.speech_url, data=flac_file, headers=self.headers)
            # get response
            # need to split string because response contains two jsons
            response = '\n'.join(urllib2.urlopen(request).read().split('\n')[1:])
        except urllib2.HTTPError as e:
            print("Exception caught: ")
            print(e)
            request.get_method()
            exit(0)
        # get text from response
        #TODO consider case where audio file is so small there's nothing to send over (ie, tap on mic)
        try:
            return json.loads(response)['result'][0]['alternative'][0]['transcript']
        except IndexError as e:
            raise NoParsableSpeech("no parsable speech, try again...")
        except ValueError as e:
            raise NoParsableSpeech("no parsable speech, try again...")

    def test_sound(self):
        """
        tool to test the sound intensity in the room
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=1, rate=self.rate,
                        input=True, output=True,
                        frames_per_buffer=self.chunk_size)
        num_silent = 0
        snd_started = False
        record_started = False

        # 'h' specifies signed short int for array type
        r = array('h')

        try:
            while 1:
                # little endian, signed short
                snd_data = array('h', stream.read(self.chunk_size))
                if byteorder == 'big':
                    snd_data.byteswap()

                print(max(snd_data)) 

        except KeyboardInterrupt as e:
            print("ctrl+c caught, exiting gracefully like swan")
            stream.stop_stream()
            stream.close()
            p.terminate()
            return True

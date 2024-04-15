# -*- coding: utf-8 -*-
import logging
import speech_recognition as sr

class VoiceRecord:
    def __init__(self):
        self.wav_num = 0
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
    def audio_Sphinx(self,filename):
        logging.info('开始识别语音文件...')
        # use the audio file as the audio source
        with sr.AudioFile(filename) as source:
            audio = self.r.record(source)  # read the entire audio file

        # recognize speech using Sphinx
        try:
            print("Sphinx thinks you said: " + self.r.recognize_sphinx(audio, language='zh-cn'))
            return self.r.recognize_sphinx(audio, language='zh-cn')
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            return None
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            return None
    def device_list(self):
        print(sr.__version__)
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    def record(self):
        while True:
            r = sr.Recognizer()
            # 启用麦克风
            mic = sr.Microphone()
            logging.info('录音中...')
            with mic as source:
                # 降噪
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            with open(f"00{self.wav_num}.wav", "wb") as f:
                # 将麦克风录到的声音保存为wav文件
                f.write(audio.get_wav_data(convert_rate=16000))
            logging.info('录音结束，识别中...')

            target = self.audio_Sphinx(f"00{self.wav_num}.wav")
            self.wav_num += 1

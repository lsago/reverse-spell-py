#!/usr/bin/env python3
# Mostly from: https://cloud.google.com/text-to-speech/docs/samples/tts-quickstart

from google.cloud import texttospeech
import simpleaudio as sa
import wave
import io
import random
import string

def ssml2audio(client, ssml, voice, audio_config):
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    return response.audio_content


def text2audio(client, text, voice, audio_config):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    return response.audio_content


def audio2file(text, audio, prepath="."):
    with open(prepath + "/" + text + '.mp3', 'wb') as out:
        out.write(audio)
        print('Audio content written to file "' + text + '.mp3' + '"')


def gen_letters_audio():
    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.VoiceSelectionParams(language_code='en_US', name='en-US-Wavenet-E')

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)

    for letter in string.ascii_lowercase:
        audio = text2audio(client, letter, voice, audio_config)
        audio2file(letter, audio, prepath='letters_audio')


def spell_word(word):
    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.VoiceSelectionParams(
        language_code='en_US',
        name='en-US-Wavenet-J'
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    word_ssml = '''
    <speak>
        <say-as interpret-as="characters">{0}</say-as>
        <break time="200ms"/>
    </speak>
    '''.format(word)
    # < break
    # time = "400ms" / >
    # {0}

    audio_word = ssml2audio(client, word_ssml, voice, audio_config)

    play_audio(audio_word)


def play_audio(audio):
    memfile = io.BytesIO(audio)
    wave_read = wave.open(memfile, 'rb')
    wave_obj = sa.WaveObject.from_wave_read(wave_read)
    # wave_obj = sa.WaveObject(audio, 1, 4, 24000)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def main():
    word_filepath = "/usr/share/dict/american-english"
    with open(word_filepath, 'r') as words_file:
        words = words_file.read().splitlines()

        word = words[random.randint(0, len(words))]
        while 4 < len(word) > 6 or word[1] != 'a':
            word = words[random.randint(0, len(words))]

        print(word)
        spell_word(word)


if __name__ == "__main__":
    main()



from datetime import datetime
import subprocess
import random

import sim800

import messages
import writer   
import polly_handler
import speech_handler
import sound_handler


# TODO: init modem
modem = sim800.SIM800()


def play_sentences( sentences ):
    files = polly_handler.render_sentences(
        sentences
    )
    sound_handler.play_files( files )
    

def handle_call():

    generated_sentences = writer.get_opening_statements()
    random.shuffle( generated_sentences )

    # generate sentence texts
    sentences = [
        messages.greeting(),            # 'good morning.' 
        "We are the algorithms."
        # generated_sentences[0],
        # messages.random_statement(),
        # generated_sentences[1],
        # generated_sentences[2],
        # messages.random_statement()
    ]

    play_sentences( sentences )
    
    while True:

        play_sentences( [messages.prompt] )  # 'what would you like to know about?'

        # wait for the user to say something
        sh = speech_handler.SpeechHandler()
        transcribed = sh.recognize()

        if transcribed is not None:
            # generate some statements about that thing
            sentences = writer.get_statements_for_subject( transcribed )
            random.shuffle( sentences )
            play_sentences( sentences[:4] )


def runloop():
    while True:
        sim800


if __name__ == "__main__":
    handle_call()


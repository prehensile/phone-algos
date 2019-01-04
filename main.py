from datetime import datetime
import subprocess
import random

from sim800 import iteadsim800

import messages
import writer   
import polly_handler
import speech_handler
import sound_handler


SOUND_DEVICE = "alsa:device=hw=1.0"


def play_sentences( sentences ):
    files = polly_handler.render_sentences(
        sentences
    )
    sound_handler.play_files(
        files,
        device = SOUND_DEVICE
    )
    

def handle_call():

    generated_sentences = writer.get_opening_statements()
    random.shuffle( generated_sentences )

    # generate sentence texts
    sentences = [
        messages.greeting(),            # 'good morning.' 
        "We are the algorithms.",
        generated_sentences[0],
        messages.random_statement(),
        generated_sentences[1],
        generated_sentences[2],
        messages.random_statement()
    ]

    play_sentences( sentences )
    
    return
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

    modem = iteadsim800.IteadSIM800()
    modem.startup()

    while True:

        # wait for a call
        print( "Waiting for a call..." )
        modem.waitForRing()

        # answer the phone
        modem.answerIncomingCall()

        # interact!
        handle_call()

        print( "Hang up!" )
        modem.hangUpCall()


if __name__ == "__main__":
    # handle_call()
    runloop()


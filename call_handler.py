import random

import messages
import writer   
import polly_handler
import speech_handler
import sound_handler


class CallHandler( object ):
    
    def __init__( self, sound_device = None ):
        self._sound_device = sound_device


    def handle_call( self ):

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

        self.play_sentences( sentences )
        
        return
        while True:

            self.play_sentences( [messages.prompt] )  # 'what would you like to know about?'

            # wait for the user to say something
            sh = speech_handler.SpeechHandler()
            transcribed = sh.recognize()

            if transcribed is not None:
                # generate some statements about that thing
                sentences = writer.get_statements_for_subject( transcribed )
                random.shuffle( sentences )
                self.play_sentences( sentences[:4] )
    

    def play_sentences( self, sentences ):
        files = polly_handler.render_sentences(
            sentences
        )
        sound_handler.play_files(
            files,
            device = self._sound_device
        )

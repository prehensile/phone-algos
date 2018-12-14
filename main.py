from datetime import datetime
import subprocess
import random

import messages
import bing_handler
import writer   
import polly_handler


# TODO: init modem

# TODO: wait for call


def play_file( pth_file ):
    args = [ "mplayer", pth_file ]
    subprocess.call( args )


def handle_call():

    generated_sentences = writer.get_opening_statements()
    random.shuffle( generated_sentences )

    # generate sentence texts
    sentences = [
        messages.greeting(),            # 'good morning.' 
        "We are the algorithms.",
        messages.random_statement(),
        generated_sentences[0],
        generated_sentences[1],
        generated_sentences[2],
        messages.random_statement(),    
        messages.prompt                 # 'what would you like to know about?'
    ]

    print( sentences )
    
    # get filenames for rendered sentences
    fn_sentences = polly_handler.render_sentences(
        sentences
    )

    # play those files!
    for fn_sentence in fn_sentences:
        play_file( fn_sentence )
    
    # wait for the user to say something
    # TODO
    
    # generate some statements about that thing
    # TODO


if __name__ == "__main__":
    handle_call()
import subprocess
import glob
import time
import glob
import random

import pygame



class SoundHandler( object ):


    def __init__( self, sound_device=None ):
        pygame.init()
        pygame.mixer.init()


    def play_file( self, pth_file, queue = False, find_matches=True ):
        
        files = [ pth_file ]

        # chorus mode
        if find_matches:

            # find files whose sentence checksum (first part of filename) matches pth_file
            prefix = pth_file.split( '.' )[0]
            matches = glob.glob(
                '{}.*'.format( prefix )
            )

            # limit matches to 3
            match_limit = 2
            if len( matches ) > match_limit:
                matches = random.sample( matches, match_limit )
            
            # add matches to list of files to play
            files.extend( matches )
        
        # create Sound and Channel objects for every file
        channels = []
        for f in files:
            s = pygame.mixer.Sound( file=f )
            c = s.play()
            channels.append( c )
        
        # block until all files have played
        busy = True
        while busy:
            b = False
            for c in channels:
                b = b or c.get_busy()
            busy = b
        
                



    def play_files( self, fn_sentences ):
        for fn_sentence in fn_sentences:
            self.play_file(
                fn_sentence
            )


if __name__ == "__main__":
    files = glob.glob( "cache/*.mp3" )
    #play_files( files[3], "alsa:device=hw=1.0" )
    sh = SoundHandler( "alsa:device=hw=1.0" )
    sh.play_files( files[:3] )

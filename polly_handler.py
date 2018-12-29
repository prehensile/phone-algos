import string
import os
import json
import random

import boto3


def cache_path( fn ):
    return os.path.join(
        os.path.realpath( "./cache" ),
        fn
    )


consonants = "bcdfghjklmnpqrstvwxyz"
file_ext = "mp3"

def path_for_sentence( sentence, voice_id ):
    
    fn = "%s%s" % (sentence, voice_id)
    fn = ''.join([l for l in fn.lower() if l in consonants])
    
    return cache_path( "%s.%s" % (fn,file_ext) )


def get_client():
    return boto3.Session(
        region_name='eu-west-1'
    ).client('polly')


def random_voice():

    all_voices = None

    fn_cached = cache_path( "voices.json" )
    if os.path.exists( fn_cached ):
        with open( fn_cached ) as fp:
            all_voices = json.load( fp )
    else:
        polly_client = get_client()
        all_voices = polly_client.describe_voices()
        with open( fn_cached, "w" ) as fp:
            json.dump( all_voices, fp )

    voices = []
    voice_blacklist = [ 'Joey', 'Justin', 'Ivy', 'Kimberly', "Joanna" ]

    for voice in all_voices["Voices"]:
        if voice['LanguageCode'].startswith( "en-"):
            voice_id = voice['Id']
            if voice_id not in voice_blacklist:
                voices.append( voice_id )
    
    return random.choice( voices )


def render_sentence( sentence, voice_id="Brian" ):

    polly_client = get_client()

    response = polly_client.synthesize_speech(
        VoiceId = voice_id,
        OutputFormat = "mp3", 
        Text = sentence
    )

    fn = path_for_sentence( sentence, voice_id )

    with open( fn, 'wb' ) as fp:
        fp.write( response['AudioStream'].read() )

    return fn

def render_sentences( sentences ): 
    rendered_paths = []
    for sentence in sentences:
        rendered_paths.append( 
            render_sentence(
                sentence,
                voice_id = random_voice()
            )
        )
    return rendered_paths

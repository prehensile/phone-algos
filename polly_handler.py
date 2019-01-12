import string
import os
import json
import random
import hashlib
from collections import namedtuple
import glob

import boto3


AudioFormat = namedtuple( "AudioFormat", ["OutputFormat","file_extension"] )

format_ogg = AudioFormat(
    OutputFormat = "ogg_vorbis",
    file_extension = "ogg"
)

format_mp3 = AudioFormat(
    OutputFormat = "mp3",
    file_extension = "mp3"
)

AUDIO_FORMAT_DEFAULT = format_ogg


def cache_path( fn ):
    return os.path.join(
        os.path.realpath( "./cache" ),
        fn
    )


def hash_for_string( str_in ):
    return hashlib.md5( str_in.encode('utf-8') ).hexdigest()


def path_for_sentence( sentence, voice_id, audio_format ):
    
    fn = "{}.{}.{}".format(
        hash_for_string( sentence ),
        voice_id,
        audio_format.file_extension
    )
    
    return cache_path( fn )


def get_client():

    creds = None
    with open( "config/aws.json" ) as fp:
        creds = json.load( fp )
    print( creds )

    return boto3.Session(
        region_name='eu-west-1',
        aws_access_key_id = creds['access_key_id'],
        aws_secret_access_key = creds['secret_access_key']
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


def render_sentence( sentence, voice_id="Brian", audio_format=AUDIO_FORMAT_DEFAULT ):

    polly_client = get_client()

    response = polly_client.synthesize_speech(
        VoiceId = voice_id,
        OutputFormat = audio_format.OutputFormat, 
        Text = sentence
    )

    fn = path_for_sentence( sentence, voice_id, audio_format )

    with open( fn, 'wb' ) as fp:
        fp.write( response['AudioStream'].read() )

    return fn


def render_sentences( sentences, audio_format=AUDIO_FORMAT_DEFAULT ): 
    rendered_paths = []
    for sentence in sentences:

        fn = render_sentence(
            sentence,
            voice_id = random_voice(),
            audio_format = audio_format
        ) 

        rendered_paths.append(fn)
    
    return rendered_paths

import subprocess


def play_file( pth_file, device=None ):
    
    args = [ "mplayer" ]
    
    if device is not None:
        args.extend( ["-ao", device] )
    
    args.append( pth_file )

    subprocess.call( args )


def play_files( fn_sentences, device=None ):
    for fn_sentence in fn_sentences:
        play_file(
            fn_sentence,
            device = device
        )

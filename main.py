from multiprocessing import Process

import call_handler

from sim800 import iteadsim800


SOUND_DEVICE = "alsa:device=hw=1.0"


class CallHandlerProcess( Process ):
    
    def __init__( self, sound_device=None ):
        super( CallHandlerProcess, self ).__init__()
        self._call_handler = call_handler.CallHandler(
            sound_device = sound_device
        )

    def run( self ):
        self._call_handler.handle_call()


handler_process = CallHandlerProcess(
    sound_device=SOUND_DEVICE
)


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
        handler_process.start()
        handler_process.join()

        print( "Hang up!" )
        modem.hangUpCall()


if __name__ == "__main__":
    # handle_call()
    # runloop()
    print( "handler process start!")
    handler_process.start()
    handler_process.join()
    print( "handler process done")


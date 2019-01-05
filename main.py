import call_handler

from sim800 import iteadsim800


SOUND_DEVICE = "alsa:device=hw=1.0"

handler = call_handler.CallHandler( sound_device=SOUND_DEVICE )


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
        handler.handle_call()

        print( "Hang up!" )
        modem.hangUpCall()


if __name__ == "__main__":
    # handle_call()
    runloop()


from multiprocessing import Process, Event

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


class ModemCallHandlerProcess( Process ):

    def __init__( self, modem=None ):
        super( ModemCallHandlerProcess, self ).__init__()
        self._modem = modem
        self.hangup_flag = Event()
        self._stopped = Event()

    def run( self ):
        print( "ModemCallHandlerProcess.run()...")
        self._stopped.clear()
        while not self._stopped.is_set():
            line = self._modem.getLine()
            if line == "NO CARRIER":
                print( line )
                self.hangup_flag.set()

    def stop( self ):
        self._stopped.set()


def runloop():

    modem = iteadsim800.IteadSIM800()
    modem.startup()
    modem_process = ModemCallHandlerProcess( modem )


    while True:

        # wait for a call
        print( "Waiting for a call..." )
        modem.waitForRing()

        # answer the phone
        modem.answerIncomingCall()

        # set up threads
        # handler_process.start()
        modem_process.start()

        # interact!
        print( "Enter runloop....")
        running = True
        while running:

            if modem_process.hangup_flag.is_set():
                # TODO: more graceful shutdown
                # handler_process.terminate()
                print( "Modem process hangup flag is set!"  )
                running = False
            
            # if not handler_process.is_alive():
            #     modem_process.terminate()
            #     modem.hangUpCall()
            #     running = False
        
        print( "runloop end ")
        

if __name__ == "__main__":
    # handle_call()
    runloop()
    # print( "handler process start!")
    # handler_process.start()
    # handler_process.join()
    # print( "handler process done")


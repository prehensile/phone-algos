import json
import speech_recognition as sr

class SpeechHandler( object ):

    def __init__( self ):
        self._gcp_credentials = None


    def gcp_credentials( self ):
        if self._gcp_credentials is None:
            with open( "config/gcp-credentials.json") as fp:
                self._gcp_credentials = fp.read()
        return self._gcp_credentials


    def recognize( self, device_index=None ):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone( device_index=device_index ) as source:
            print("Say something!")
            audio = r.listen(source)

        transcribed = None
        try:
            transcribed = r.recognize_google_cloud(
                audio,
                credentials_json = self.gcp_credentials()
            )
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))

        print( transcribed )

        return transcribed
    

    def list_microphones( self ):
        return sr.Microphone.list_microphone_names()


    def get_microphone_index_by_name( self, name ):
        for index, list_name in enumerate( self.list_microphones() ):
            if name in list_name:
                return( index )


if __name__ == "__main__":
    sh = SpeechHandler()
    m = sh.list_microphones()
    print( m )
    print( sh.get_microphone_index_by_name("hw:1,0") )

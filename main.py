# pip install spherov2
# pip install bleak
# pip install SpeechRecognition
# brew install portaudio
# pip install pyaudio

import bluetooth
import speech
import journalbot01

# sphero operations
# from spherov2 import scanner
# from spherov2.sphero_edu import SpheroEduAPI
# from spherov2.types import Color

def main():
    # Print out all of the nearby Sphero robots
    bluetooth.find_sphero()
    # exit()

    SPHERO_ADDRESS_1 = "B00FBF73-5AA0-4586-D91C-309F7E3CBD77" # Dan's sphero
    SPHERO_ADDRESS_2 = "304EFFEF-1EEF-7515-112F-B54A11AAEE08" # Michael's sphero
    SPHERO_ADDRESS_3 = "E614CA17-73A4-1989-260D-0085379D73E9" # Michael's sphero?
    SPHERO_ADDRESS_4 = "121B52A1-0684-8A2A-149A-787D01EFD952" # Dan's sphero?
    toy = bluetooth.select_sphero(SPHERO_ADDRESS_3)
    
    if toy != None:
        # run(toy)
        journalbot01.start_program(toy)
    else:
        print("Couldn't find robot..")

def run(toy):
    # Connect to the toy and control it using SpheroEduAPI
    with SpheroEduAPI(toy) as sphero:
        sphero.set_main_led(Color(255, 0, 0))  # Set LED color to red
        # text = speech.capture_speech()
        speech.start_listening()
        sphero.set_main_led(Color(0, 0, 0))    # Turn off the LED


if __name__ == "__main__":
    main()

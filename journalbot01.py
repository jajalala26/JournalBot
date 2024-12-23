import time
import pyttsx3
import speech
from spherov2.sphero_edu import SpheroEduAPI, EventType
from spherov2.types import Color
from textblob import TextBlob
import prompts

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 125) 

# Listen to user input (Placeholder for input system)
def listen():
    return speech.start_listening()

# Sentiment analysis (Simulated here)
def analyze_sentiment(user_input):
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "I'm not sure what you mean."

# Main function to start the journaling session
def start_journaling_session(droid):
    journaling = True
    count = 0


    while journaling:
        lumin = droid.get_luminosity()
        if lumin['ambient_light'] <= 3:
            print(droid.get_luminosity)
            prompts.text_to_speech("sleepy")
            journaling = False
            return

        user_input = listen()
        time.sleep(2)
        if "box breathing" in user_input:
            print("recognize breathing")
            box_breathing(droid, 3)

        prompts.back_n_forth(user_input, count)



            

        count +=1
        time.sleep(1)

def set_matrix(matrix, droid):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            droid.set_matrix_fill(x, y, x, y, Color(matrix[x][y][0], matrix[x][y][1], matrix[x][y][2]))

def set_lines(droid, breathe_in):
    if breathe_in:
        for x in range(8):
            droid.set_matrix_line(x, 0, x, 7, Color(173, 216, 230))
            time.sleep(0.45)
    else:
        for x in range(8, -1, -1):
            droid.set_matrix_line(x, 0, x, 7, Color(0, 0, 0))
            time.sleep(0.45)

pattern = [
    [(34, 214, 156), (255, 200, 100), (120, 155, 220), (50, 100, 200), (255, 0, 200), (35, 75, 255), (150, 180, 255), (10, 200, 50)],
    [(30, 180, 100), (90, 60, 255), (220, 180, 50), (255, 255, 0), (25, 0, 180), (200, 100, 50), (180, 100, 200), (80, 60, 255)],
    [(255, 0, 0), (200, 0, 0), (0, 0, 255), (255, 255, 255), (30, 180, 255), (100, 200, 0), (70, 100, 255), (50, 0, 255)],
    [(50, 100, 150), (50, 150, 200), (255, 255, 100), (200, 0, 255), (255, 120, 0), (100, 200, 255), (150, 200, 0), (0, 100, 50)],
    [(120, 200, 50), (100, 200, 150), (30, 200, 255), (255, 100, 50), (50, 200, 255), (180, 50, 200), (200, 0, 0), (255, 255, 255)],
    [(0, 255, 255), (0, 255, 50), (180, 255, 100), (100, 0, 255), (200, 200, 255), (0, 200, 255), (50, 255, 255), (150, 200, 0)],
    [(200, 0, 150), (255, 50, 0), (50, 50, 255), (0, 0, 0), (255, 100, 0), (0, 255, 255), (255, 0, 200), (50, 200, 150)],
    [(255, 0, 255), (100, 200, 255), (0, 255, 100), (50, 100, 150), (100, 200, 255), (200, 150, 0), (255, 255, 0), (200, 0, 255)]
]


def box_breathing(droid, reps):
    # orient
    droid.set_front_led(Color(255, 255, 255))
    prompts.text_to_speech("Please place me in front of my to your left, with the LED pointing right")
    time.sleep(3)

    for x in range(reps):
        # breathe in    
        prompts.text_to_speech("Breathe in")
        droid.set_front_led(Color(0, 0, 0))
        droid.set_heading(0)
        droid.set_speed(40)
        set_lines(droid, True)
        # time.sleep(4)
        # hold
        prompts.text_to_speech("Hold")
        droid.set_front_led(Color(173, 216, 230))
        droid.set_back_led(Color(173, 216, 230))
        droid.set_speed(0)
        time.sleep(4)
        # breathe out
        prompts.text_to_speech("Breathe out")
        droid.set_front_led(Color(0, 0, 0))
        droid.set_back_led(Color(0, 0, 0))
        droid.set_heading(180)
        droid.set_speed(40)
        set_lines(droid, False)
        # time.sleep(4)
        # hold
        prompts.text_to_speech("Hold")
        droid.set_front_led(Color(173, 216, 230))
        droid.set_back_led(Color(173, 216, 230))
        droid.set_speed(0)
        time.sleep(4)

def on_charging(droid):
    droid.set_main_led(Color(6, 0, 255))
    prompts.text_to_speech('charging')
    
    time.sleep(1)
    prompts.text_to_speech('remove me from my charger')

# Program to start
def start_program(toy):
  with SpheroEduAPI(toy) as droid:
      # Set LED and matrix animation as a startup effect
      droid.set_main_led(Color(r=0, g=0, b=0))
      start_journaling_session(droid)

# Run the program
if __name__ == "__main__":
    start_program()

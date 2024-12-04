import time
import random
import pyttsx3
import speech
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from textblob import TextBlob
import prompts

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 125) 

def text_to_speech(message):
    """Use TTS to read the text aloud."""
    tts_engine.say(message)
    tts_engine.runAndWait()

# Listen to user input (Placeholder for input system)
def listen():
    # commands = [
    #     "start journal", "I've been feeling really grateful for my family.",
    #     "I was busy today", "Today was tough.", "terminate"
    # ]
    return speech.start_listening()
    # return random.choice(commands)

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

# Determine response based on sentiment
def determine_response(sentiment):
    if sentiment == "positive":
        text_to_speech("I'm glad to hear that! It's always great to enjoy the moment. Would you like to elaborate more on what specific moments made today enjoyable?")
    elif sentiment == "negative":
        text_to_speech("Even though today wasn't the best, you always have tomorrow to look forward to. What are you excited for tomorrow?")
    else:
        text_to_speech("Thank you for sharing. Journaling is a great way to relax and express ourselves. What are you grateful for today?")

# Main function to start the journaling session
def start_journaling_session(droid):
    journaling = True
    count = 0
    max_iterations = 5

    while journaling:# and (count < max_iterations):
        user_input = listen()
        time.sleep(5)
        ###### add if else to check for specific input #######
        if "box breathing" in user_input:
            print("recognize breathing")
            # text_to_speech("How many repetitions would you like?")
            # user_input = listen()
            box_breathing(droid, 3)
        prompts.back_n_forth(max_iterations)
            
        ######################################################
        # sentiment = analyze_sentiment(user_input)
        # time.sleep(1)
        # determine_response(sentiment)
        # time.sleep(1)

        if user_input == "terminate":
            journaling = False
            text_to_speech("Thanks for journaling with me. Goodbye!")

        # count += 1
        # if count >= max_iterations and journaling:
        #     text_to_speech("Ending session to prevent infinite loop in prototype.")
        #     journaling = False

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
    text_to_speech("Please place me in front of my to your left, with the LED pointing right")
    time.sleep(3)

    for x in range(reps):
        # breathe in    
        text_to_speech("Breathe in")
        droid.set_front_led(Color(0, 0, 0))
        droid.set_heading(0)
        droid.set_speed(40)
        set_lines(droid, True)
        # time.sleep(4)
        # hold
        text_to_speech("Hold")
        droid.set_front_led(Color(173, 216, 230))
        droid.set_back_led(Color(173, 216, 230))
        droid.set_speed(0)
        time.sleep(4)
        # breathe out
        text_to_speech("Breathe out")
        droid.set_front_led(Color(0, 0, 0))
        droid.set_back_led(Color(0, 0, 0))
        droid.set_heading(180)
        droid.set_speed(40)
        set_lines(droid, False)
        # time.sleep(4)
        # hold
        text_to_speech("Hold")
        droid.set_front_led(Color(173, 216, 230))
        droid.set_back_led(Color(173, 216, 230))
        droid.set_speed(0)
        time.sleep(4)
    

    

# Program to start
def start_program(toy):
    # Find toy and connect
    # toy = scanner.find_toy()
    with SpheroEduAPI(toy) as droid:
        # Set LED and matrix animation as a startup effect
        droid.set_main_led(Color(r=0, g=0, b=0))
        # droid.set_matrix_fill(0, 0, 3, 3, Color(r=255, g=0, b=0))
        
        # droid.set_matrix_line(0, 0, 0, 7, Color(173, 216, 230))
        # droid.set_matrix_character()
        # box_breathing(droid)
        
        # set_matrix(pattern, droid)
        # text_to_speech("Robot connected, beginning journaling session!")
        # time.sleep(1)

        # # Start the journaling session
        # text_to_speech("What do you want to talk about today? How are you feeling?")
        start_journaling_session(droid)

# Run the program
if __name__ == "__main__":
    start_program()

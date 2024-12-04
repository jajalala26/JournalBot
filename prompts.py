from textblob import TextBlob
import speech
import time
import pyttsx3
import random



tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 125) 

def listen():
    # commands = [
    #     "start journal", "I've been feeling really grateful for my family.",
    #     "I was busy today", "Today was tough.", "terminate"
    # ]
    return speech.start_listening()

def text_to_speech(message):
    """Use TTS to read the text aloud."""
    tts_engine.say(message)
    tts_engine.runAndWait()

def analyze_sentiment(user_input):
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "I'm not sure what you mean."

def determine_response(sentiment):
    if sentiment == "positive":
        text_to_speech("I'm glad to hear that! It's always great to enjoy the moment. Would you like to elaborate more on what specific moments made today enjoyable?")
    elif sentiment == "negative":
        text_to_speech("Even though today wasn't the best, you always have tomorrow to look forward to. What are you excited for tomorrow?")
    else:
        text_to_speech("Thank you for sharing. Journaling is a great way to relax and express ourselves. What are you grateful for today?")
        
def prompt(sentiment, count):
    positive_response = ["That's wonderful to hear!",
     "Gratitude can really shift our perspective, thank you for sharing!", 
     "What a great outlook!",
     "You're radiating positivity today - keep it up!",
     "That's so inspiring-thank you for sharing such a lovely thought!",
     "This is a great reflection",
     "Your mindset is inspiring"
    ]

    negative_response = ["Your feelings are valid, and it's great that you're expressing them." ,
    "Recognizing these things is so important. You're doing great.",
    "I'm here to listen if you want to share more about this.",
    "Thank you for sharing."]

    neutral_response = ["That's such a thoughtful insight",
     "Reflecting is so meaningful", 
     "Interesting point! Do you want to dive deeper into it?",
     "I appreciate your openness.",
     "It's great to see you exploring this." ,
    "Thanks for noting this."]

    neutral_prompts = [
        "What did you learn today, big or small?",
        "How was your day today?",
        "How are you feeling right now, and why?",
        "What place makes you feel most peaceful? Describe that place using all five senses.",
        "What about your work feels real, necessary, or important to you?",
        "How do you make time for yourself each day?"
    ]

    uplifting_prompts = [
        "How did you take care of yourself today?",
        "What's one thing that made you smile today?",
        "What's one thing you're proud of from today?",
        "What do you appreciate most about your personality? What aspects do you find harder to accept?",
        "What three ordinary things bring you the most joy?"
    ]

    if count == 0:
        text_to_speech(neutral_prompts[
            random.randint(0, (len(neutral_prompts) - 1))])
    elif sentiment == "neutral" and count != 0:
      text_to_speech(neutral_response[
            random.randint(0, (len(neutral_response) - 1))])
      text_to_speech(neutral_prompts[
            random.randint(0, (len(neutral_prompts) - 1))])
    elif sentiment == "negative":
      text_to_speech(negative_response[
            random.randint(0, (len(negative_response) - 1))])
      text_to_speech(uplifting_prompts[
            random.randint(0, (len(uplifting_prompts) - 1))])
    else:
      text_to_speech(positive_response[
          random.randint(0, (len(positive_response) - 1))])
      text_to_speech(uplifting_prompts[
          random.randint(0, (len(uplifting_prompts) - 1))])
    return

def back_n_forth(max_iterations):
    user_input = listen()

    count = 0
    sentiment = analyze_sentiment(user_input)
    time.sleep(1)
    prompt(sentiment, count)
    time.sleep(1)

    if user_input == "terminate":
        journaling = False
        text_to_speech("Thanks for journaling with me. Goodbye!")

    count += 1
    if count >= max_iterations and journaling:
        text_to_speech("Ending session to prevent infinite loop in prototype.")
        journaling = False

    time.sleep(1)
    return

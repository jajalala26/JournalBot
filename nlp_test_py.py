from textblob import TextBlob

def get_response(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "I’m so glad to hear that! Keep up the positive energy!"
    elif polarity < 0:
        return "I’m sorry you feel that way. I’m here if you want to talk."
    else:
        return "I’m not sure what you mean."

# Test the model
# print(get_response("I feel great!"))  # Positive Test
# print(get_response("I feel terrible..."))  # Negative Test
# print(get_response("goodbye for now"))  # Neutral Test

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye! Take care.")
        break
    response = get_response(user_input)
    print(f"Bot: {response}")

import time
import openai

SECRET_KEY = "API key"  # Replace it with your own API key for your ChatGPT account.
# You can find the API key of your ChatGPT account at the following URL：
# https://platform.openai.com/account/api-keys

openai.api_key = SECRET_KEY
MAX_TOKEN_LEN = 1024    # The maximum number of tokens (words or symbols) allowed in a single response from the chatbot
TIME_OUT = 3            # The number of seconds to wait for a response from the chatbot API before timing out

ROLE = 'assistant'
USER_ROLE = 'user'
PROMPT = f'you are {ROLE}.'


# Define a class for the chatbot
class MyChatBot:
    def __init__(self) -> None:
        self.messages = []   # A list to keep track of the conversation history
        self.reset_log()     # Reset the conversation history

    # Receive a message from the OpenAI Chat API
    def receive_message_from_api(self):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0301',   # The name of the OpenAI language model to use
            messages=self.messages,       # The conversation history so far
            temperature=1.0,              # Controls the creativity of the chatbot's responses
            max_tokens=MAX_TOKEN_LEN,     # The maximum number of tokens (words or symbols) allowed in a single response from the chatbot
            top_p=0.6,                    # Controls the diversity of the chatbot's responses
            frequency_penalty=2.0,        # Penalizes the chatbot for using frequently occurring words
            presence_penalty=0.0,         # Penalizes the chatbot for using words that don't occur very often
            stream=True,                  # Enable streaming responses from the chat API
            timeout=TIME_OUT,             # The number of seconds to wait for a response from the chatbot API before timing out
        )
        return response

    # Get a response from the chatbot given a prompt
    def get_response(self, prompt):
        self.add_user_content(prompt)   # Add the user's input to the conversation history
        stream_response = self.receive_message_from_api()
        return stream_response

    # Reset the conversation history
    def reset_log(self):
        self.messages = [{'role': 'system', 'content': PROMPT}]

    # Add the user's input to the conversation history
    def add_user_content(self, content):
        self.messages.append({'role': USER_ROLE, 'content': content})

    # Add the chatbot's response to the conversation history
    def add_bot_content(self, content):
        self.messages.append({'role': ROLE, 'content': content})


# Define a class for the chat session
class Chat:
    def __init__(self):
        chatbot = MyChatBot()

        # Set chatbot to an instance variable
        self.chatbot = chatbot

    def chatting(self):
        # Get user input and store it in a variable called input_text
        input_text = input("You:")

        # Call the get_response method from the MyChatBot class to get a response from the chatbot
        stream_response = self.chatbot.get_response(input_text)

        # Initialize a variable called answer to store the chatbot's response
        answer = ""

        # Initialize a variable called timeout_cnt to keep track of how many times the program has timed out
        timeout_cnt = 0

        # Continuously get the stream response until it is complete or the program times out
        while True:
            try:
                # Get the next package in the stream response
                package = next(stream_response)

                # Check if the package has a finish reason of "stop"
                if package.choices[0].finish_reason == "stop":
                    # If the package has a finish reason of "stop", break out of the loop
                    break

                # Check if the package has an attribute called "role"
                if hasattr(package.choices[0].delta, 'role'):
                    # If the package has an attribute called "role", continue to the next iteration of the loop
                    continue

                # Get the content of the first delta in the package
                single_token = package.choices[0].delta.content

                # Add the content to the answer variable
                answer += single_token
            except:
                # If the response is incomplete, wait for 1 second and try again.
                if len(answer) > 0:
                    break
                timeout_cnt += 1
                if timeout_cnt >= TIME_OUT:
                    break
                time.sleep(1)

        # Add the bot's response to conversation history.
        self.chatbot.add_bot_content(answer)

        # Print the chatbot's response
        print(answer)
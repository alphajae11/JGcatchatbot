# Documentation of CatBot

## Backend Processing for APIs
### OpenAI Assistant API
The Cat Chatbot utilizes the OpenAI Assistant API to create a dynamic and interactive chatbot experience. Here's how it works:

1. Assistant Creation:

- An OpenAI Assistant is created once using the create_assistant() function in assistantcatbot.py.
- The Assistant is configured with specific instructions to act as a cat-loving chatbot and is equipped with a custom function get_cat_image.


2. Thread Management:

- For each user interaction, a new thread is created using openai.beta.threads.create().
- This ensures that each conversation is isolated and maintains its own context.


3. Message Processing:

- User messages are added to the thread using openai.beta.threads.messages.create().
- The Assistant processes these messages within the context of the thread.


4. Run Execution:

- The openai.beta.threads.runs.create() function initiates the Assistant's processing of the thread.
- The application polls the run status until it's completed or requires action.


5. Function Calling:

- If the Assistant determines that a cat image is needed, it calls the get_cat_image function.
- The results are then submitted back to the Assistant using openai.beta.threads.runs.submit_tool_outputs().


6. Response Retrieval:

- Once processing is complete, the Assistant's response is retrieved from the thread and streamed back to the user.

### Cat API
The Cat API is integrated to fetch cat images based on the Assistant's requests. Here's how it's implemented:

1. API Integration:

- The get_cat_image() function in cat_image.py handles interactions with The Cat API.
- It uses the requests library to make HTTP GET requests to the API.

2. Parameter Handling:

- The function accepts optional breed and count parameters to customize the image request.
- These parameters are passed as query parameters in the API request.

3. Response Processing:

- The API response is parsed to extract image URLs.
- If successful, a list of image URLs is returned.
- In case of an error, an empty list is returned, and the error is logged.

### Handling Response Process

## Frontend Interface
### CatBot Frontend Interface Design and Implementation
The frontend interface is designed to provide a seamless and interactive chat experience. Here's a breakdown of the key components:

1. DOM Structure:

- #status: Displays current status of the Assistant's processing.
- #chat-container: Main container for the chat interface. 
  - #chat-messages: Holds the conversation history. 
  - #chat-form: Contains the input field and send button.
- #cat-image-container: Displays fetched cat images.

2. JavaScript Implementation (chat.js):

Event Listeners:
- DOMContentLoaded: Initializes the chat interface.
- Form submission: Handles user messages.


Key Functions:
- sendMessageStream(): Sends user message and handles streaming response.
- addMessage(): Adds messages to the chat interface.
- updateStatus(): Updates the status display.
- updateBotMessage(): Updates or adds bot responses.
- displayCatImages(): Renders fetched cat images.

Processing and Returning Messages:
- User messages are immediately displayed in the chat interface.
- Bot responses are streamed and updated in real-time.
- Status updates are displayed separately from the chat messages.
- Cat images, when fetched, are displayed in a dedicated container.

2. Why Streaming didn't work as I thought (Suggestion) and how I tried to make up for it (Status)

*Resources*:
- To start with OpenAI API call
  - https://platform.openai.com/docs/quickstart?desktop-os=macOS&language-preference=python&quickstart-example=completions
- About Assistant API
  - https://platform.openai.com/docs/assistants/quickstart
  - https://platform.openai.com/docs/assistants/deep-dive
- Function Calling
  - https://platform.openai.com/docs/guides/function-calling
- CatAPI regarding breeds
  - https://api.thecatapi.com/v1/breeds
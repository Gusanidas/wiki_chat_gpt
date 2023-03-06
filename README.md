# Wiki Chat Gpt

This is a simple chat app that uses the OpenAI ChatGPT API to generate responses based on user prompts, with additional context from Wikipedia pages.
The idea is to experiment how providing data through the prompt can make ChatGPT less prone to make up information.
The app is built using Python and requires an OpenAI API key.

## Getting Started

To run the chat app, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set the environment variables for your OpenAI. You can use a `.env` file to store these variables, and load them using the `python-dotenv` package.
  The required environment variables are:
  
```
 OPENAI_API_KEY=<your_api_key>
```

For now the only way to run it is as a cli app, just run:

```
python cli_chat.py
```

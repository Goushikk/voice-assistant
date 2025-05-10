# AI Voice Assistant

This is a simple AI voice assistant built using Python and various libraries for wake word detection, speech-to-text, natural language processing, and text-to-speech. It features a graphical user interface (GUI) built with Tkinter.

## Features

* **Wake Word Detection:** Listens for a specific wake word ("Hey Assistant" by default, configurable via `WAKE_WORD_PATH`).
* **Speech-to-Text:** Transcribes spoken audio into text using the Whisper model.
* **Natural Language Processing:** Sends transcribed text to OpenAI's GPT-3.5-turbo model for generating responses.
* **Text-to-Speech:** Speaks the AI's response using the `pyttsx3` library.
* **Basic Command Execution:** Includes functionality to open Google, YouTube, and Notepad via voice commands.
* **Microphone Sensitivity Adjustment:** Allows users to adjust the microphone sensitivity through a GUI slider.
* **VU Meter:** Provides a visual representation of the microphone input level.
* **Conversation Logging:** Records user input and assistant responses to a log file (`conversation_logs.txt`).
* **Simple GUI:** Offers a user-friendly interface for interaction and status updates.

## Prerequisites

Before running the assistant, ensure you have the following installed:

* **Python 3.x**
* **Required Python Libraries:**
    ```bash
    pip install tkinter sounddevice numpy whisper openai pvporcupine pyttsx3 scipy webbrowser
    ```
* **Picovoice Access Key:** You need a valid access key from [Picovoice Console](https://console.picovoice.ai/) to use the Porcupine wake word engine. Replace `"YOUR_PORCUPINE_ACCESS_KEY"` in the script with your actual key.
* **OpenAI API Key:** You need an API key from [OpenAI](https://openai.com/api/) to use the GPT-3.5-turbo model. Replace `"YOUR_OPENAI_API_KEY"` in the script with your actual key.
* **Wake Word File (.ppn):** Download a wake word file (e.g., "hey-assistant.ppn") from the [Picovoice Console](https://console.picovoice.ai/) and place it at the path specified by `WAKE_WORD_PATH` in the script.

## Setup

1.  **Clone or Download:** Download the Python script (`index.py`) to your local machine.
2.  **Install Dependencies:** If you haven't already, install the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt  # If you create a requirements.txt file
    # OR
    pip install tkinter sounddevice numpy whisper openai pvporcupine pyttsx3 scipy webbrowser
    ```
3.  **Configure API Keys and Wake Word Path:**
    * Open the Python script in a text editor.
    * Replace `"YOUR_OPENAI_API_KEY"` with your OpenAI API key.
    * Replace `"YOUR_PORCUPINE_ACCESS_KEY"` with your Picovoice Access Key.
    * Ensure that `WAKE_WORD_PATH` correctly points to the location of your `.ppn` wake word file. If it's in the same directory, `"hey-assistant.ppn"` should suffice (assuming you named it that).

## Running the Assistant

1.  **Execute the Script:** Open your terminal or command prompt, navigate to the directory where you saved the script, and run:
    ```bash
    python index.py
    ```
    
2.  **Using the Assistant:**
    * The GUI window will appear, displaying the status as "Waiting for wake word".
    * Speak the configured wake word (default is "Hey Assistant").
    * The assistant should respond with "Yes?" and the status will change to "Listening...".
    * Clearly speak your question or command.
    * The transcribed text will appear in the text box, followed by the assistant's response.
    * The assistant will also speak its response.
    * Basic commands like "open google", "open youtube", and "open notepad" will trigger the corresponding actions.
    * The microphone sensitivity can be adjusted using the slider.

## Configuration

The following variables in the script can be configured:

* `openai.api_key`: Your OpenAI API key.
* `ACCESS_KEY`: Your Picovoice Access Key.
* `WAKE_WORD_PATH`: The path to your `.ppn` wake word file.
* `WHISPER_MODEL`: The Whisper model to use for speech-to-text (e.g., "tiny", "base", "small", "medium", "large"). "base" is the default.
* `LOG_FILE`: The name of the file where conversation logs will be saved (default is "conversation_logs.txt").

## Troubleshooting

* **No Audio Input:** Ensure your microphone is properly connected and that your operating system allows the Python script to access it. You might need to check your system's audio settings.
* **Wake Word Not Detected:** Make sure the `WAKE_WORD_PATH` is correct and that you are speaking the wake word clearly. Adjusting microphone sensitivity might also help.
* **OpenAI API Errors:** Verify your API key is correct and that you have sufficient credits in your OpenAI account.
* **Picovoice Errors:** Ensure your access key is correct and that the wake word file is valid.
* **Text-to-Speech Issues:** Check if the `pyttsx3` engine is initialized correctly and if your system has the necessary speech synthesis components.

## Further Development

This is a basic implementation and can be extended with more features, such as:

* More sophisticated command execution.
* Contextual awareness and memory of previous conversations.
* Integration with other APIs and services.
* Customizable voice for text-to-speech.
* Improved error handling and logging.
* More advanced GUI features.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

Copyright © [2025] [Goushik Krishna]

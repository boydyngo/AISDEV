# AI-Powered Text and Audio Tool (Python Version)

This is the Python desktop version of the AI-Powered Text and Audio Tool, designed to improve text and audio workflows for users who need accessibility features, content creators, and anyone who works extensively with text and audio.

## Features

- **Text-to-Speech (TTS)**: Convert text to natural-sounding audio with customizable voices and playback controls
- **Speech-to-Text (STT)**: Transcribe audio recordings or dictate text in real-time
- **Text Transformation**: Translate text, correct grammar, and rewrite content in different styles
- **Clipboard Management**: Retain history of copied text items and access quick actions
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **AI Assistant**: Ask general questions and receive AI-powered answers

## Prerequisites

- Python 3.8 or higher
- PyQt6
- Other dependencies as listed in requirements.txt

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-text-audio-tool.git
cd ai-text-audio-tool/python-version
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit the `.env` file in the `config` directory with your API keys and preferences:

```
OPENAI_API_KEY=your_openai_api_key_here
MAX_CLIPBOARD_HISTORY=10
DEFAULT_VOICE=Default Male
TOKEN_COST_WARNING_THRESHOLD=1000
DEFAULT_DARK_MODE=False
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Running the Application

```bash
python main.py
```

## Usage

- **Text-to-Speech**: Enter text in the main text area and use the TTS module to convert it to speech
- **Dark Mode**: Toggle between light and dark themes using the View menu > Toggle Dark Mode option

## Token Usage and Costs

AI features in this application consume tokens which may incur costs if you're using a paid API key. The application displays estimated token usage before performing AI operations to help you manage costs.

## Building a Standalone Executable

You can create a standalone executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```

The executable will be created in the `dist` directory.

## License

[Your License Here]
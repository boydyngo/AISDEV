# AI-Powered Text and Audio Tool (Web Version)

This is the web version of the AI-Powered Text and Audio Tool, designed to improve text and audio workflows for users who need accessibility features, content creators, and anyone who works extensively with text and audio.

## Features

- **Text-to-Speech (TTS)**: Convert text to natural-sounding audio with customizable voices and playback controls
- **Speech-to-Text (STT)**: Transcribe audio recordings or dictate text in real-time
- **Text Transformation**: Translate text, correct grammar, and rewrite content in different styles
- **Clipboard Management**: Retain history of copied text items and access quick actions
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **AI Assistant**: Ask general questions and receive AI-powered answers

## Prerequisites

- Node.js (v16 or higher)
- npm (v8 or higher)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-text-audio-tool.git
cd ai-text-audio-tool/web-version
```

### 2. Install frontend dependencies

```bash
cd client
npm install
```

### 3. Install backend dependencies

```bash
cd ../server
npm install
```

### 4. Configure environment variables

Create a `.env` file in the `server` directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
PORT=5000
MAX_CLIPBOARD_HISTORY=10
DEFAULT_VOICE=default-male
TOKEN_COST_WARNING_THRESHOLD=1000
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Running the Application

### 1. Start the backend server

```bash
cd server
npm run dev
```

The server will start on http://localhost:5000.

### 2. Start the frontend application

```bash
cd client
npm start
```

The application will open in your browser at http://localhost:3000.

## Usage

- **Text-to-Speech**: Enter text in the main text area and use the TTS module to convert it to speech
- **Dark Mode**: Toggle between light and dark themes using the sun/moon icon in the app bar

## Token Usage and Costs

AI features in this application consume tokens which may incur costs if you're using a paid API key. The application displays estimated token usage before performing AI operations to help you manage costs.

## License

[Your License Here]
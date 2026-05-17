## 📰 ➡️ 🎙️ Blog to Podcast Agent

A Streamlit app that converts any blog post into a listenable podcast episode. Paste a URL, get an AI-summarized audio file you can play or download.

## Features

- **Blog Scraping**: Fetches content from any public blog URL (direct scrape + Jina Reader fallback).
- **Summary Generation**: Condenses the article into a conversational podcast script using `gpt-4o-mini`.
- **Text-to-Speech**: Converts the script to audio using `gpt-4o-mini-tts` with your choice of voice.
- **Download**: Save the generated podcast as an MP3.

## Requirements

- Python 3.8+
- An OpenAI API key — or a compatible proxy (see below)

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run blog_to_podcast_agent.py
```

## Using a Proxy (yunwu.ai)

If you can't access the OpenAI API directly, you can use a relay such as [yunwu.ai](https://yunwu.ai):

1. Get your API key from [yunwu.ai](https://yunwu.ai)
2. In the app sidebar:
   - **OpenAI API Key**: enter your yunwu.ai key
   - **Base URL**: change to `https://yunwu.ai/v1`
3. Everything else works the same — the app calls `gpt-4o-mini` and `gpt-4o-mini-tts` through the relay.

## Configuration

| Sidebar field | Default | Description |
|---|---|---|
| OpenAI API Key | — | Your OpenAI or proxy API key |
| Base URL | `https://api.openai.com/v1` | Change to `https://yunwu.ai/v1` for relay |
| Voice | `nova` | alloy / echo / fable / onyx / nova / shimmer |

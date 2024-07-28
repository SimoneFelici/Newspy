# Newspy

Newspy is a console-based news scraping and summarization tool designed to provide a streamlined and informative reading experience.

## Description

Newspy allows users to browse and read articles from various websites directly from the console, with the capability to generate AI summaries of the articles.
The application is designed to be lightweight, fast, and respectful of user privacy.

## Key Features

- **News Scraping**: Extracts content from predefined websites or manually entered URLs.
- **Privacy**: Offers a clean reading experience without ads or tracking.
- **Image Rendering**: Supports image display directly in the terminal (only with Kitty).
- **AI Summaries**: Generates concise summaries of articles using the OpenAI API.
- **Modularity**: Flexible structure that allows easy addition of new websites and features.
- **Cool**: Terminal ui>>>

## Requirements

- Python 3.x
- Kitty terminal (for displaying images)
- OpenAI API key (for AI summaries)

## Installation

1. Clone the repository: ```git clone https://github.com/SimoneFelici/Newspy.git```
2. Install dependencies: ```pip install -r requirements.txt```
3. Edit the `.env` file in the directory and add your OpenAI API key, or choose if you want to display images:

## Usage

Run the main script: ```python3 main.py```

## License

GNU v3.0

# Astrology Chatbot 🔮

A mystical Streamlit-based chatbot powered by Google Gemini AI that provides personalized astrology readings, horoscope predictions, zodiac insights, and cosmic guidance.

## Features ✨

- **Zodiac Sign Readings**: Detailed insights into all 12 zodiac signs
- **Daily Horoscopes**: Personalized daily predictions for your sign
- **Compatibility Analysis**: Check romantic and friendship compatibility between signs
- **Birth Chart Interpretation**: Detailed analysis based on birth date, time, and location
- **Planetary Guidance**: Understand planetary transits and their effects
- **Interactive Chat**: Natural conversation with an AI astrologer
- **Beautiful UI**: Cosmic-themed interface with interactive elements

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd path/to/astrology_chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Open `astrology_chatbot.py` and replace `"AIzaSyDZnf3yvP30HHUQd8kqc_-_8abP6KVTaEk"` with your own API key
   - Or set it as an environment variable (recommended for production)

## Usage 🌟

### Run the Chatbot

```bash
streamlit run astrology_chatbot.py
```

The app will open in your default browser at `http://localhost:8501`

### Using the Chatbot

1. **Set Your Cosmic Profile** (optional but recommended)
   - Enter your birth date to reveal your zodiac sign
   - Add birth time and location for more detailed readings
   - Add your name for personalized interactions

2. **Choose Your Reading**
   - Use quick tools in the sidebar for popular readings
   - Or ask any astrology question in the chat

3. **Explore Zodiac Signs**
   - Browse all 12 zodiac signs in the Zodiac tab
   - Get instant readings for any sign
   - Learn about elements, rulers, and compatibility

## Available Quick Tools 🛠️

- **Daily Horoscope**: Get your personalized daily reading
- **Zodiac Sign Info**: Learn about all zodiac signs
- **Compatibility Check**: Analyze compatibility with another sign
- **Clear Chat**: Reset the conversation

## Supported Topics

- ♈ Zodiac sign characteristics and personality traits
- 📊 Horoscope readings (daily, weekly, monthly, yearly)
- 🎯 Birth chart interpretation
- 💕 Zodiac compatibility (romantic, friendship, professional)
- 🌙 Lunar phases and their effects
- 👑 Planetary transits and influences
- ✨ Tarot card meanings
- 🔢 Numerology basics
- 🏠 Astrological houses and aspects

## Example Questions

- "What is my horoscope for today?"
- "Tell me about my birth chart"
- "What's the compatibility between Aries and Scorpio?"
- "What should I expect this week?"
- "Describe the characteristics of a Gemini"
- "What do the current planetary transits mean?"
- "Is this a good time for new beginnings?"

## Requirements 📦

- streamlit>=1.38.0
- google-generativeai>=0.7.2
- python-dotenv>=1.0.1

## Troubleshooting 🔧

### API Key Error
- Make sure your Google Gemini API key is valid
- Check that the key is correctly placed in the code
- Verify you have internet connectivity

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Make sure you're using the activated virtual environment

### Port Already in Use
```bash
# Run on a different port
streamlit run astrology_chatbot.py --server.port 8502
```

## Project Structure

```
astrology_chatbot/
├── astrology_chatbot.py      # Main chatbot application
├── genai_example.py          # Reference example for Gemini API
├── requirements.txt          # Project dependencies
├── README.md                 # This file
└── .env                      # API keys (create this file)
```

## Security Notes ⚠️

- **Never commit your API key** to version control
- Use environment variables for sensitive data in production
- Consider using a `.env` file and python-dotenv for local development

## Creating a .env File (Optional)

1. Create a `.env` file in the project directory
2. Add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Update the code to load from environment:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   API_KEY = os.getenv("GOOGLE_API_KEY")
   ```

## Performance Tips ⚡

- Chat history is stored in session state and will persist during a session
- Longer conversations may take slightly more time for responses
- Clear chat history if you want to start fresh
- Bookmark the app for quick access

## Customization 🎨

You can customize:
- Colors and styling (edit the CSS in the `st.markdown()` section)
- System prompt (modify the `ASTROLOGY_PROMPT` variable)
- Zodiac information (update `ZODIAC_SIGNS` dictionary)
- Button labels and UI text

## License

This project is provided as-is for educational and personal use.

## Support & Contributing

For issues, suggestions, or improvements, feel free to modify and extend the code!

---

**Made with ✨ and 🔮 | Powered by Google Gemini AI**

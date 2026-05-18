"""
Enhanced Astrology Chatbot using Streamlit and Google Gemini API
Features: Zodiac readings, horoscopes, birth chart analysis, and more
"""
import streamlit as st
from datetime import datetime
import importlib
import json
import sys

# Check if running with Streamlit
try:
    if not st.runtime.exists():
        print("This script must be run with Streamlit. Use: streamlit run astrology_chatbot.py")
        sys.exit(1)
except AttributeError:
    print("This script must be run with Streamlit. Use: streamlit run astrology_chatbot.py")
    sys.exit(1)

# Load either google.genai or google.generativeai
try:
    from google import genai
    GENAI_IMPLEMENTATION = "genai"
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_IMPLEMENTATION = "generativeai"
    except ImportError as exc:
        raise ImportError(
            "Could not import google.genai or google.generativeai. "
            "Install one of these packages in the environment used to run Streamlit."
        ) from exc

# Page configuration
st.set_page_config(
    page_title="✨ Astrology Chatbot",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chat history and client
if "messages" not in st.session_state:
    st.session_state.messages = []

if "genai_impl" not in st.session_state:
    API_KEY = "AIzaSyDZnf3yvP30HHUQd8kqc_-_8abP6KVTaEk"
    st.session_state.genai_impl = GENAI_IMPLEMENTATION
    st.session_state.genai_module = genai
    st.session_state.model = "gemini-2.5-flash"

    if GENAI_IMPLEMENTATION == "genai":
        st.session_state.client = genai.Client(api_key=API_KEY)
    else:
        genai.configure(api_key=API_KEY)
        st.session_state.client = genai

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# Custom CSS for enhanced styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0a1a 0%, #1a0a2e 50%, #2d1b4e 100%);
        color: #e0d5ff;
    }
    
    .main-container {
        background: rgba(20, 10, 40, 0.6);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(147, 112, 219, 0.2);
    }
    
    .title {
        text-align: center;
        color: #FFD700;
        font-size: 3em;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #9370DB;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .subtitle {
        text-align: center;
        color: #DDA0DD;
        font-size: 1.3em;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #DDA0DD;
    }
    
    .zodiac-info {
        background: rgba(147, 112, 219, 0.1);
        border: 2px solid #9370DB;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .horoscope-card {
        background: rgba(255, 215, 0, 0.05);
        border-left: 4px solid #FFD700;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .chat-input-container {
        margin-top: 20px;
    }
    
    .bot-typing {
        color: #FFD700;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Zodiac information
ZODIAC_SIGNS = {
    "Aries": {"dates": "Mar 21 - Apr 19", "emoji": "♈", "element": "Fire", "ruler": "Mars"},
    "Taurus": {"dates": "Apr 20 - May 20", "emoji": "♉", "element": "Earth", "ruler": "Venus"},
    "Gemini": {"dates": "May 21 - Jun 20", "emoji": "♊", "element": "Air", "ruler": "Mercury"},
    "Cancer": {"dates": "Jun 21 - Jul 22", "emoji": "♋", "element": "Water", "ruler": "Moon"},
    "Leo": {"dates": "Jul 23 - Aug 22", "emoji": "♌", "element": "Fire", "ruler": "Sun"},
    "Virgo": {"dates": "Aug 23 - Sep 22", "emoji": "♍", "element": "Earth", "ruler": "Mercury"},
    "Libra": {"dates": "Sep 23 - Oct 22", "emoji": "♎", "element": "Air", "ruler": "Venus"},
    "Scorpio": {"dates": "Oct 23 - Nov 21", "emoji": "♏", "element": "Water", "ruler": "Pluto"},
    "Sagittarius": {"dates": "Nov 22 - Dec 21", "emoji": "♐", "element": "Fire", "ruler": "Jupiter"},
    "Capricorn": {"dates": "Dec 22 - Jan 19", "emoji": "♑", "element": "Earth", "ruler": "Saturn"},
    "Aquarius": {"dates": "Jan 20 - Feb 18", "emoji": "♒", "element": "Air", "ruler": "Uranus"},
    "Pisces": {"dates": "Feb 19 - Mar 20", "emoji": "♓", "element": "Water", "ruler": "Neptune"}
}

# Astrology system prompt
ASTROLOGY_PROMPT = """You are an expert Astrology Chatbot with deep knowledge of:
- Western Astrology (Zodiac signs, houses, aspects, transits)
- Planetary positions and their meanings
- Birth chart interpretation and analysis
- Horoscope readings (daily, weekly, monthly)
- Zodiac sign characteristics and personality traits
- Compatibility between signs (romantic, friendship, professional)
- Lunar phases and their effects
- Numerology basics
- Tarot card meanings

Provide insightful, accurate, and helpful astrology readings. Be warm, engaging, and mystical while maintaining astrological accuracy.
When users ask about their zodiac sign or birth chart, ask for their birth date, time, and place if needed for detailed readings.
Always provide practical and positive guidance. Use emojis sparingly but meaningfully to enhance responses.
Format your responses clearly with headers when discussing multiple aspects.
End readings with encouraging or uplifting messages."""

def get_astrology_response(user_input: str) -> str:
    """Get response from Gemini API"""
    try:
        # Combine system prompt with user input and user profile if available
        user_context = ""
        if st.session_state.user_profile:
            user_context = f"\n\nUser Profile:\n{json.dumps(st.session_state.user_profile)}"
        
        full_prompt = f"{ASTROLOGY_PROMPT}{user_context}\n\nUser: {user_input}\n\nAstrologer:"

        if st.session_state.genai_impl == "genai":
            response = st.session_state.client.models.generate_content(
                model=st.session_state.model,
                contents=full_prompt
            )
        else:
            model = st.session_state.client.GenerativeModel(
                model_name=st.session_state.model
            )
            response = model.generate_content(full_prompt)

        return getattr(response, "text", str(response))
    except Exception as e:
        return f"🔮 *The stars are currently obscured...* \n\n**Error:** {str(e)}\n\nPlease try again later or check your API key."

def get_zodiac_from_date(month: int, day: int) -> str:
    """Determine zodiac sign from birth date"""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

# Main title and header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="title">🔮 Astrology Chatbot 🔮</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Cosmic Guide to the Stars</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar with user profile and quick actions
with st.sidebar:
    st.title("✨ Astrology Hub")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "♈ Zodiac", "🛠️ Tools"])
    
    with tab1:
        st.subheader("Your Cosmic Profile")
        
        # User profile setup
        col1, col2 = st.columns(2)
        with col1:
            birth_month = st.selectbox("Birth Month", 
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x-1])
        
        with col2:
            birth_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        
        if birth_month and birth_day:
            zodiac = get_zodiac_from_date(birth_month, birth_day)
            st.session_state.user_profile["zodiac_sign"] = zodiac
            st.session_state.user_profile["birth_date"] = f"{birth_month}/{birth_day}"
            
            # Display zodiac info
            if zodiac in ZODIAC_SIGNS:
                info = ZODIAC_SIGNS[zodiac]
                st.markdown(f"""
                **Your Sign:** {info['emoji']} **{zodiac}**
                
                📅 **Dates:** {info['dates']}
                🔥 **Element:** {info['element']}
                👑 **Ruler:** {info['ruler']}
                """)
        
        birth_year = st.number_input("Birth Year (optional)", 
                                     min_value=1900, 
                                     max_value=datetime.now().year,
                                     value=2000)
        if birth_year:
            st.session_state.user_profile["birth_year"] = birth_year
        
        birth_time = st.time_input("Birth Time (optional)")
        if birth_time:
            st.session_state.user_profile["birth_time"] = str(birth_time)
        
        birth_place = st.text_input("Birth Place (optional)", placeholder="City, Country")
        if birth_place:
            st.session_state.user_profile["birth_place"] = birth_place
        
        name = st.text_input("Your Name (optional)", placeholder="Enter your name")
        if name:
            st.session_state.user_profile["name"] = name
    
    with tab2:
        st.subheader("Zodiac Signs")
        search_zodiac = st.selectbox("Find a Sign", list(ZODIAC_SIGNS.keys()))
        
        if search_zodiac:
            info = ZODIAC_SIGNS[search_zodiac]
            st.markdown(f"""
            ### {info['emoji']} {search_zodiac}
            
            **Dates:** {info['dates']}
            **Element:** {info['element']}
            **Planetary Ruler:** {info['ruler']}
            """)
            
            if st.button(f"Get {search_zodiac} Reading"):
                user_query = f"Give me a detailed reading about {search_zodiac} zodiac sign, including personality traits, strengths, weaknesses, and compatibility with other signs."
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": get_astrology_response(user_query)
                })
                st.rerun()
    
    with tab3:
        st.subheader("Quick Tools")
        
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📅 Daily Horoscope", use_container_width=True):
            if st.session_state.user_profile.get("zodiac_sign"):
                zodiac = st.session_state.user_profile["zodiac_sign"]
                user_query = f"Give me a detailed daily horoscope for {zodiac} for today. Include lucky hours, colors, and recommendations."
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": get_astrology_response(user_query)
                })
                st.rerun()
            else:
                st.warning("Please set your birth month and day first!")
        
        if st.button("💕 Compatibility Check", use_container_width=True):
            other_sign = st.selectbox("Compare with:", list(ZODIAC_SIGNS.keys()))
            if st.session_state.user_profile.get("zodiac_sign"):
                my_sign = st.session_state.user_profile["zodiac_sign"]
                user_query = f"Analyze the compatibility between {my_sign} and {other_sign}. Include romantic, friendship, and professional compatibility."
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": get_astrology_response(user_query)
                })
                st.rerun()
            else:
                st.warning("Please set your birth month and day first!")
        
        st.markdown("---")
        st.markdown("### 📚 About This Bot")
        st.markdown("""
        This mystical chatbot provides:
        - 🔮 Zodiac sign readings
        - 📊 Horoscope predictions
        - 🎯 Birth chart insights
        - 💕 Compatibility analysis
        - 🌙 Planetary guidance
        - ✨ Tarot insights
        """)

# Main chat area
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🔮" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your zodiac sign, horoscope, birth chart, or any astrology question..."):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Get and display bot response
    with st.chat_message("assistant", avatar="🔮"):
        with st.spinner("✨ Consulting the cosmic forces..."):
            response = get_astrology_response(prompt)
            st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

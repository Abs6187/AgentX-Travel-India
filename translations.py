import streamlit as st
import time
from streamlit.components.v1 import html

def show_progress_bar(text="Loading..."):
    progress_html = f"""
    <style>
    .progress-container {{
        width: 100%;
        background: linear-gradient(45deg, #FF671F, #046A38);
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .progress-bar {{
        width: 0%;
        height: 25px;
        background: linear-gradient(45deg, #046A38, #FF671F);
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
        position: relative;
        overflow: hidden;
    }}
    .progress-bar::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.1) 0%,
            rgba(255,255,255,0.3) 50%,
            rgba(255,255,255,0.1) 100%);
        animation: shimmer 2s infinite;
    }}
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    .progress-text {{
        color: #FFFFFF;
        text-align: center;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-bottom: 5px;
    }}
    </style>
    <div class="progress-container">
        <div class="progress-text">{text}</div>
        <div class="progress-bar"></div>
    </div>
    <script>
        const progressBar = document.querySelector('.progress-bar');
        let progress = 0;
        const interval = setInterval(() => {{
            progress += 1;
            progressBar.style.width = progress + '%';
            if (progress >= 100) {{
                clearInterval(interval);
            }}
        }}, 50);
    </script>
    """
    html(progress_html, height=100)

translations = {
    "en": {
        "welcome": "Welcome to AgentX-Travel India!",
        "loading": "Planning your perfect Indian adventure...",
        "destination_prompt": "Where in India would you like to explore?",
        "examples": [
            "Plan a weekend trip to the Taj Mahal in Agra",
            "Find budget-friendly hotels in Goa",
            "Create an itinerary for Kerala backwaters",
            "Suggest local food spots in Mumbai",
            "Plan a spiritual journey to Varanasi"
        ],
        "progress_messages": [
            "Consulting with local travel experts...",
            "Checking availability of heritage hotels...",
            "Finding the best street food recommendations...",
            "Planning temple visits and cultural experiences...",
            "Organizing transportation via Indian Railways..."
        ]
    }
}

def get_translation(key, lang="en"):
    """
    Get a translation for a specific key in the specified language.
    
    Args:
        key (str): The translation key to look up
        lang (str): Language code (always en now)
        
    Returns:
        str: The translated text in English
    """
    return translations["en"].get(key, key)
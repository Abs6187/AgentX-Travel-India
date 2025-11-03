"""
# AgentX-Travel India
# ------------------
# An AI-powered travel assistant application tailored for the Indian market
# Created by TechMatrix Solvers for IIITDMJ HackByte3.0 (April 4-6, 2025)
#
# Features:
# - Personalized travel itinerary generation using AI agents
# - Bilingual support (English and Hindi)
# - India-specific travel recommendations
# - Interactive maps and visualizations
# - Downloadable travel plans
#
# Team:
# - Abhay Gupta (Team Leader)
# - Jay Kumar
# - Kripanshu Gupta
# - Aditi Soni
#
# This application uses:
# - Streamlit for the frontend
# - LangChain for AI orchestration
# - Google Generative AI (Gemini) for language processing
# - Geopy for location services
# - Pydeck for map visualizations
"""

import os
import sys

# Initialize MongoDB, OpenAI and MCP availability flags as False by default
# These will be set to True only if the imports succeed
MONGODB_AVAILABLE = False
OPENAI_AVAILABLE = False
MCP_AVAILABLE = False

# Debugging information for deployment troubleshooting
print("Python version:", sys.version)
print("Working directory:", os.getcwd())
print("Directory contents:", os.listdir())
print("Environment variables:", [(k, v) for k, v in os.environ.items() if 'SECRET' not in k.upper()])

try:
    import streamlit as st
    print("Streamlit version:", st.__version__)
except Exception as e:
    print(f"Error importing streamlit: {str(e)}")
    sys.exit(1)  # Exit if Streamlit isn't available - it's required

# Continue with the rest of the imports
try:
    import json
    from datetime import datetime, timedelta
    import base64
    import pandas as pd
    import pydeck as pdk
    import requests
    from travel import (
        destination_research_task, accommodation_task, transportation_task,
        activities_task, dining_task, itinerary_task, chatbot_task,
        run_task
    )
    from geopy.geocoders import Nominatim
    
    # Try to import MongoDB modules - but make them optional
    try:
        from pymongo import MongoClient
        from bson import ObjectId
        MONGODB_AVAILABLE = True
        print("MongoDB integration available")
    except ImportError:
        MONGODB_AVAILABLE = False
        print("MongoDB integration not available")
        
    # Try to import OpenAI module - but make it optional
    try:
        from openai import OpenAI
        OPENAI_AVAILABLE = True
        print("OpenAI integration available")
    except ImportError:
        OPENAI_AVAILABLE = False
        print("OpenAI integration not available")
        
    # Try to import MCP module - but make it optional
    try:
        from mcp.client import ClientSession, WebSocketServerParameters
        import mcp.types as mcp_types
        import asyncio
        MCP_AVAILABLE = True
        print("MCP integration available")
    except ImportError:
        MCP_AVAILABLE = False
        print("MCP integration not available")
        
except Exception as e:
    print(f"Error during imports: {str(e)}")
    # Don't exit here - we'll handle missing dependencies gracefully

st.set_page_config(
    page_title="Your AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    /* Custom progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #FF671F; /* Indian saffron color */
        background-image: linear-gradient(45deg, #FF671F, #046A38, #FF671F); /* Tricolor-inspired gradient */
        background-size: 300% 300%;
        animation: progress-bar-animation 3s ease infinite;
    }
    
    @keyframes progress-bar-animation {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }
    
    /* Output text color */
    .output-text {
        color: #2E4053; /* Deep blue color for text */
        font-size: 1.1em;
    }
    
    /* Custom output background */
    .output-container {
        background-color: #f9f7f3; /* Light cream color */
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #FF671F; /* Indian saffron border */
        margin-bottom: 20px;
    }
    
    /* Chat message styling */
    .ai-message {
        background-color: #e8f4ea !important; /* Light green background for AI */
        border-left: 4px solid #046A38 !important; /* Green border */
    }
    
    .user-message {
        background-color: #fff7e6 !important; /* Light orange background for user */
        border-left: 4px solid #FF671F !important; /* Saffron border */
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Add logo to the header
logo_col1, logo_col2 = st.columns([1, 4])
with logo_col1:
    # Check if logo file exists before trying to load it
    logo_path = os.path.join(os.path.dirname(__file__), "android-chrome-512x512.png")
    if os.path.exists(logo_path):
        try:
            st.image(logo_path, width=100)
        except Exception as e:
            # If image fails to load, show emoji as fallback
            st.markdown("# ✈️")
    else:
        # If image doesn't exist, show emoji as fallback
        st.markdown("# ✈️")
with logo_col2:
    st.markdown("## " + t("page_title"))
    st.markdown("##### AI-powered travel assistant for India")

# ------------------------------------------
# Translation dictionary and helper functions
# ------------------------------------------
translations = {
    "en": {
         "page_title": "Your AI Travel Assistant",
         "header": "Your AI Travel Assistant",
         "create_itinerary": "Create Your Itinerary",
         "trip_details": "Trip Details",
         "origin": "Origin",
         "destination": "Destination",
         "travel_dates": "Travel Dates",
         "duration": "Duration (days)",
         "preferences": "Preferences",
         "additional_preferences": "Additional Preferences",
         "interests": "Interests",
         "special_requirements": "Special Requirements",
         "submit": "🚀 Create My Personal Travel Itinerary",
         "request_details": "Your Travel Request",
         "from": "From",
         "when": "When",
         "budget": "Budget",
         "travel_style": "Travel Style",
         "live_agent_outputs": "Live Agent Outputs",
         "full_itinerary": "Full Itinerary",
         "details": "Details",
         "download_share": "Download & Share",
         "save_itinerary": "Save Your Itinerary",
         "plan_another_trip": "🔄 Plan Another Trip",
         "about": "About",
         "how_it_works": "How it works",
         "travel_agents": "Travel Agents",
         "share_itinerary": "Share Your Itinerary",
         "save_for_mobile": "Save for Mobile",
         "built_with": "Built with ❤️ in India",
         "itinerary_ready": "Your Travel Itinerary is Ready! 🎉",
         "personalized_experience": "We've created a personalized travel experience just for you. Explore your itinerary below.",
         "agent_activity": "Agent Activity",
         "error_origin_destination": "Please enter both origin and destination.",
         "your_itinerary_file": "Your Itinerary File",
         "text_format": "Text format - Can be opened in any text editor",
         "settings": "Settings",
         "map_view": "Map View",
         "chat": "Chat with AI",
         "download_itinerary": "Download Itinerary",
         "download_format": "Download Format",
         "copy_to_clipboard": "Copy to Clipboard",
         "copied": "Copied!",
         "gemini_api_key": "Google AI (Gemini) API Key",
         "enter_api_key": "Enter your Gemini API key",
         "api_key_updated": "API key updated!",
         "api_key_required": "Required for AI functionality. Get a key at https://ai.google.dev/"
    }
}

def t(key):
    return translations["en"].get(key, key)

# ------------------------------------------
# Initialize all session state variables
# ------------------------------------------
def initialize_session_state():
    """Initialize all required session state variables."""
    if 'generated_itinerary' not in st.session_state:
        st.session_state.generated_itinerary = None
        
    # Set language to English always
    st.session_state.language = 'en'
    st.session_state.selected_language = "en"
        
    if 'step_results' not in st.session_state:
        st.session_state.step_results = {}
    
    # Ensure step_results has all required keys
    for key in ["destination_research", "accommodation", "transportation", "activities", "dining", "itinerary"]:
        if key not in st.session_state.step_results:
            st.session_state.step_results[key] = None
            
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if "results" not in st.session_state:
        st.session_state.results = {}
        
    if "gemini_api_key" not in st.session_state:
        # Check for environment variables first
        env_key_1 = os.getenv("GEMINI_API_KEY_1")
        env_key_2 = os.getenv("GEMINI_API_KEY_2")
        fallback_key = os.getenv("GEMINI_API_KEY")

        # Use the first available key for session state
        if env_key_1:
            st.session_state.gemini_api_key = env_key_1
        elif env_key_2:
            st.session_state.gemini_api_key = env_key_2
        elif fallback_key:
            st.session_state.gemini_api_key = fallback_key
        else:
            st.session_state.gemini_api_key = ""
        
    if "tailvy_api_key" not in st.session_state:
        st.session_state.tailvy_api_key = ""
        
    if "mongodb_uri" not in st.session_state:
        st.session_state.mongodb_uri = ""
        
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
        
    if "tailvy_used" not in st.session_state:
        st.session_state.tailvy_used = False
        
    if "mongodb_used" not in st.session_state:
        st.session_state.mongodb_used = False
        
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "full_itinerary"

# Run initialization
initialize_session_state()

# Helper function to download text file
def get_download_link(text_content, filename):
    b64 = base64.b64encode(text_content.encode()).decode()
    href = f'<a class="download-link" href="data:text/plain;base64,{b64}" download="{filename}"><i>📥</i> {t("save_itinerary")}</a>'
    return href

# ------------------------------------------
# Tailvy API Integration
# ------------------------------------------
def use_tailvy_api(query, api_key, endpoint="itinerary"):
    """
    Call Tailvy API for travel planning
    
    Args:
        query (str): The travel query with trip details
        api_key (str): Tailvy API key
        endpoint (str): API endpoint to use
        
    Returns:
        dict: API response or None if failed
    """
    try:
        base_url = "https://api.tailvy.com/v1"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "query": query,
            "format": "json"
        }
        
        # Add a timeout to prevent hanging on slow API responses
        response = requests.post(f"{base_url}/{endpoint}", headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            try:
                result = response.json()
                # Validate that response has expected fields
                if endpoint == "travel" and not all(k in result for k in ["destination_info", "accommodations", "transportation"]):
                    st.warning("Tailvy API response is missing expected fields. Falling back to default method.")
                    return None
                return result
            except ValueError:
                st.warning("Tailvy API returned invalid JSON. Falling back to default method.")
                return None
        elif response.status_code == 401:
            st.error("Invalid Tailvy API key. Please check your credentials.")
            return None
        elif response.status_code == 429:
            st.warning("Tailvy API rate limit exceeded. Falling back to default method.")
            return None
        else:
            st.warning(f"Tailvy API returned status code {response.status_code}. Falling back to default method.")
            return None
    except requests.exceptions.Timeout:
        st.warning("Tailvy API request timed out. Falling back to default method.")
        return None
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to Tailvy API. Falling back to default method.")
        return None
    except Exception as e:
        st.warning(f"Error calling Tailvy API: {str(e)}. Falling back to default method.")
        return None

# ------------------------------------------
# MongoDB Integration
# ------------------------------------------
def find_nearby_attractions(destination, search_term, radius=5000):
    """
    Find attractions near the specified destination using MongoDB vector search
    
    Args:
        destination (str): The destination name (e.g., "Agra")
        search_term (str): What to search for (e.g., "historical sites")
        radius (int): Search radius in meters
        
    Returns:
        dict: MongoDB search results or None if failed
    """
    if not MONGODB_AVAILABLE or not OPENAI_AVAILABLE:
        st.warning("MongoDB or OpenAI package not installed. Can't use geo-based recommendations.")
        return None
        
    try:
        # Check if we have the required API keys
        if not st.session_state.mongodb_uri or not st.session_state.openai_api_key:
            return None
            
        # Connect to MongoDB
        client = MongoClient(st.session_state.mongodb_uri)
        db_name = 'travel_india'
        collection = client[db_name]['attractions']
        
        # Get coordinates for the destination
        geolocator = Nominatim(user_agent="travel_app")
        location = geolocator.geocode(destination)
        
        if not location:
            st.warning(f"Could not find coordinates for {destination}.")
            return None
            
        # Create the geo query
        coordinates = [location.longitude, location.latitude]
        
        # Create a new search ID for this query
        search_id = ObjectId()
        
        # Set up pipeline for geospatial pre-filtering
        geo_pipeline = [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": coordinates},
                    "distanceField": "distance",
                    "maxDistance": radius,
                    "spherical": True
                }
            },
            {
                "$addFields": {
                    "searchId": search_id
                }
            }
        ]
        
        # Execute the pre-filtering to narrow down candidates
        collection.aggregate(geo_pipeline)
        
        # Create OpenAI client and generate embeddings for the search term
        openai_client = OpenAI(api_key=st.session_state.openai_api_key)
        response = openai_client.embeddings.create(
            input=search_term,
            model="text-embedding-3-small",
            dimensions=256
        )
        search_embedding = response.data[0].embedding
        
        # Vector search among pre-filtered candidates
        vector_query = {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": search_embedding,
                "path": "embedding",
                "numCandidates": 10,
                "limit": 5,
                "filter": {"searchId": search_id}
            }
        }
        
        # Execute vector search
        results = list(collection.aggregate([vector_query]))
        
        return {
            "results": results,
            "count": len(results),
            "destination": destination,
            "coordinates": coordinates
        }
        
    except Exception as e:
        st.warning(f"Error using MongoDB search: {str(e)}")
        return None

# Add MongoDB initialization function
def initialize_mongodb_collection():
    """
    Initialize MongoDB collection with sample attraction data
    
    This function creates a sample collection of Indian attractions with
    coordinates and descriptions if it doesn't exist yet
    """
    if not MONGODB_AVAILABLE:
        st.error("MongoDB package not installed. Cannot initialize collection.")
        return False
        
    try:
        # Check if we have MongoDB connection details
        if not st.session_state.mongodb_uri:
            st.error("MongoDB connection URI is required.")
            return False
            
        # Connect to MongoDB
        client = MongoClient(st.session_state.mongodb_uri)
        db_name = 'travel_india'
        collection_name = 'attractions'
        
        # Create the database and collection if they don't exist
        db = client[db_name]
        
        # Check if collection exists and has documents
        if collection_name in db.list_collection_names() and db[collection_name].count_documents({}) > 0:
            st.success(f"Collection '{collection_name}' already exists with data.")
            return True
            
        # Create collection
        collection = db[collection_name]
        
        # Sample attraction data for India
        sample_attractions = [
            {
                "name": "Taj Mahal",
                "description": "Iconic white marble mausoleum built by Emperor Shah Jahan.",
                "location": {
                    "type": "Point",
                    "coordinates": [78.0422, 27.1751]
                },
                "city": "Agra",
                "type": "historical",
                "tags": ["monument", "UNESCO", "marble", "mughal"]
            },
            {
                "name": "Agra Fort",
                "description": "UNESCO World Heritage site, a historical fort in the city of Agra.",
                "location": {
                    "type": "Point",
                    "coordinates": [78.0254, 27.1784]
                },
                "city": "Agra",
                "type": "historical",
                "tags": ["fort", "UNESCO", "mughal", "red sandstone"]
            },
            {
                "name": "Fatehpur Sikri",
                "description": "A city founded in the 16th century by a Mughal emperor.",
                "location": {
                    "type": "Point",
                    "coordinates": [77.6701, 27.0947]
                },
                "city": "Agra",
                "type": "historical",
                "tags": ["UNESCO", "abandoned city", "mughal"]
            },
            {
                "name": "Mehtab Bagh",
                "description": "Garden complex aligned with the Taj Mahal on the opposite side of the river.",
                "location": {
                    "type": "Point",
                    "coordinates": [78.0499, 27.1792]
                },
                "city": "Agra",
                "type": "park",
                "tags": ["garden", "viewpoint", "taj mahal"]
            },
            {
                "name": "India Gate",
                "description": "War memorial dedicated to soldiers who died in WWI.",
                "location": {
                    "type": "Point",
                    "coordinates": [77.2295, 28.6129]
                },
                "city": "Delhi",
                "type": "monument",
                "tags": ["memorial", "war memorial", "landmark"]
            },
            {
                "name": "Red Fort",
                "description": "Historic fort that served as the main residence of the Mughal Emperors.",
                "location": {
                    "type": "Point",
                    "coordinates": [77.2410, 28.6562]
                },
                "city": "Delhi",
                "type": "historical",
                "tags": ["fort", "UNESCO", "mughal", "red sandstone"]
            },
            {
                "name": "Humayun's Tomb",
                "description": "The tomb of the Mughal Emperor Humayun, commissioned by his wife.",
                "location": {
                    "type": "Point",
                    "coordinates": [77.2507, 28.5933]
                },
                "city": "Delhi",
                "type": "historical",
                "tags": ["tomb", "UNESCO", "mughal", "garden"]
            },
            {
                "name": "Gateway of India",
                "description": "An arch monument built during the 20th century in Mumbai.",
                "location": {
                    "type": "Point",
                    "coordinates": [72.8347, 18.9220]
                },
                "city": "Mumbai",
                "type": "monument",
                "tags": ["arch", "colonial", "sea", "landmark"]
            },
            {
                "name": "Marine Drive",
                "description": "A 3.6-kilometer-long boulevard in South Mumbai that offers scenic views.",
                "location": {
                    "type": "Point",
                    "coordinates": [72.8217, 18.9474]
                },
                "city": "Mumbai",
                "type": "landmark",
                "tags": ["promenade", "sea view", "coast", "sunset"]
            },
            {
                "name": "Elephanta Caves",
                "description": "A collection of cave temples predominantly dedicated to the Hindu god Shiva.",
                "location": {
                    "type": "Point",
                    "coordinates": [72.9311, 18.9633]
                },
                "city": "Mumbai",
                "type": "historical",
                "tags": ["cave", "UNESCO", "hindu temple", "island"]
            }
        ]
        
        # If OPENAI_AVAILABLE, create embeddings for sample data
        if OPENAI_AVAILABLE and st.session_state.openai_api_key:
            openai_client = OpenAI(api_key=st.session_state.openai_api_key)
            with st.status("Creating vector embeddings..."):
                for attraction in sample_attractions:
                    # Create embeddings for the attraction name and description
                    embedding_text = f"{attraction['name']} {attraction['description']} {' '.join(attraction['tags'])}"
                    response = openai_client.embeddings.create(
                        input=embedding_text,
                        model="text-embedding-3-small",
                        dimensions=256
                    )
                    attraction["embedding"] = response.data[0].embedding
                
        # Insert sample data
        collection.insert_many(sample_attractions)
        
        # Create indexes
        collection.create_index([("location", "2dsphere")])
        if OPENAI_AVAILABLE and st.session_state.openai_api_key:
            # Create vector index if embeddings were added
            db.command({
                "createIndexes": collection_name,
                "indexes": [{
                    "name": "vector_index",
                    "key": {"embedding": "vector"},
                    "vectorOptions": {
                        "dimension": 256,
                        "similarity": "cosine"
                    }
                }]
            })
        
        st.success(f"Successfully created collection with {len(sample_attractions)} sample attractions.")
        return True
        
    except Exception as e:
        st.error(f"Error initializing MongoDB collection: {str(e)}")
        return False

# ------------------------------------------
# Start of Streamlit UI code
# ------------------------------------------

# Sidebar for settings
with st.sidebar:
    st.title("✈️ " + t("settings"))
    
    # Gemini API Key input
    api_key = st.text_input(
        t("gemini_api_key"),
        placeholder=t("enter_api_key"),
        type="password",
        help=t("api_key_required")
    )

    # Validate and save API key
    if api_key:
        if api_key.startswith("AI"):
            st.session_state.gemini_api_key = api_key
            st.success(t("api_key_updated"))
        else:
            st.error("Invalid API key. Gemini API keys start with 'AI'")

    # Check which environment variables are set
    env_key_1 = os.getenv("GEMINI_API_KEY_1")
    env_key_2 = os.getenv("GEMINI_API_KEY_2")

    # Show status of environment variables
    if env_key_1 or env_key_2:
        keys_detected = []
        if env_key_1:
            keys_detected.append("GEMINI_API_KEY_1 ✅")
        if env_key_2:
            keys_detected.append("GEMINI_API_KEY_2 ✅")

        st.success(f"**API Keys Detected:**\n" + "\n".join([f"- {key}" for key in keys_detected]))

        if env_key_1 and env_key_2:
            st.info("🔄 Automatic API key rotation is enabled! The system will switch between keys if rate limits are hit.")
    else:
        st.info("""
    💡 **Multiple API Keys Support**

    To avoid rate limits, you can set multiple API keys as environment variables:
    - `GEMINI_API_KEY_1` - Primary API key
    - `GEMINI_API_KEY_2` - Backup API key

    The system will automatically switch to the backup key if the primary hits rate limits.
        """)

    st.caption("**Current Model:** gemini-2.5-flash")
    
    # Add Tailvy API Key input (optional)
    st.markdown("### 🧩 Tailvy API (Optional)")
    tailvy_api_key = st.text_input(
        "Tailvy API Key",
        placeholder="Enter your Tailvy API key",
        type="password",
        help="Optional: Enhance travel recommendations with Tailvy API. Provides more detailed itineraries, local insights, and real-time availability of attractions and accommodations."
    )
    
    # Save Tailvy API key to session state
    if tailvy_api_key:
        st.session_state.tailvy_api_key = tailvy_api_key
        st.success("Tailvy API key saved!")
        
    if 'tailvy_api_key' in st.session_state and st.session_state.tailvy_api_key:
        st.info("Tailvy API integration is active! You'll receive enhanced travel recommendations.")
    else:
        st.caption("💡 Using Tailvy API provides better recommendations for Indian destinations with local expertise.")
    
    # Add MCP integration section ONLY if the modules are available
    if MCP_AVAILABLE:
        st.markdown("### 🧠 Model Context Protocol (Optional)")
        
        mcp_server_url = st.text_input(
            "MCP Server URL",
            placeholder="ws://localhost:3000",
            help="Optional: Connect to an MCP server for enhanced context-aware responses"
        )
        
        # Save MCP server URL to session state
        if mcp_server_url:
            st.session_state.mcp_server_url = mcp_server_url
            st.success("MCP server URL saved!")
            
            # Add option to test MCP connection
            if st.button("Test MCP Connection"):
                with st.spinner("Testing MCP connection..."):
                    connection_successful = test_mcp_connection(mcp_server_url)
                    if connection_successful:
                        st.session_state.mcp_connected = True
                        st.success("Successfully connected to MCP server!")
                    else:
                        st.session_state.mcp_connected = False
                        st.error("Failed to connect to MCP server. Please check the URL and ensure the server is running.")
            
            if st.session_state.get("mcp_connected", False):
                st.info("MCP integration is active! You'll receive context-aware travel recommendations.")
    else:
        st.markdown("### 🧠 Model Context Protocol (Installation Required)")
        st.warning("""
        To enable context-aware AI with the Model Context Protocol, please install:
        ```
        pip install mcp-python-sdk
        ```
        Then restart the application to access this feature.
        """)
    
    # Add MongoDB and OpenAI integration section ONLY if the modules are available
    if MONGODB_AVAILABLE and OPENAI_AVAILABLE:
        st.markdown("### 🗺️ MongoDB Geo Search (Optional)")
        
        mongodb_uri = st.text_input(
            "MongoDB Connection URI",
            placeholder="mongodb+srv://username:password@cluster...",
            type="password",
            help="Optional: Add MongoDB connection string to enable location-based attraction search"
        )
        
        openai_api_key = st.text_input(
            "OpenAI API Key",
            placeholder="sk-...",
            type="password",
            help="Required for MongoDB vector search to work properly"
        )
        
        # Save MongoDB and OpenAI credentials to session state
        if mongodb_uri:
            st.session_state.mongodb_uri = mongodb_uri
            if openai_api_key:
                st.session_state.openai_api_key = openai_api_key
                st.success("MongoDB and OpenAI credentials saved!")
                st.info("Geo-based attraction recommendations are now enabled!")
                
                # Show option to initialize sample data
                if st.button("Initialize Sample Attractions Data"):
                    initialize_mongodb_collection()
            else:
                st.warning("Please provide an OpenAI API key for vector search functionality.")
    elif not MONGODB_AVAILABLE:
        st.markdown("### 🗺️ MongoDB Geo Search (Installation Required)")
        st.warning("""
        To enable geo-based attraction search, please install:
        ```
        pip install pymongo openai
        ```
        Then restart the application to access this feature.
        """)
    elif not OPENAI_AVAILABLE:
        st.markdown("### 🗺️ MongoDB Geo Search (Installation Required)")
        st.warning("""
        To enable geo-based attraction search, please install:
        ```
        pip install openai
        ```
        Then restart the application to access this feature.
        """)
    
    # About section
    st.markdown("### ℹ️ " + t("about"))
    st.info(
        "AgentX-Travel India is an AI-powered travel assistant application tailored for the Indian market. "
        "It uses specialized AI agents to create personalized travel itineraries."
    )
    
    # Travel agents section
    st.markdown("### 🧳 " + t("travel_agents"))
    st.write(
        "Our AI system uses specialized agents for destination research, accommodations, "
        "transportation, activities, dining, and itinerary creation."
    )

# Show notification for MCP if unavailable
if not MCP_AVAILABLE:
    # Add notification about optional MCP features
    st.sidebar.markdown("""
    <div style="padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #f8f9fa; border-left: 3px solid #3366cc;">
        <b>ℹ️ Optional Feature Unavailable</b><br>
        Model Context Protocol integration is unavailable because the required packages are not installed.
        <code>pip install mcp-python-sdk</code> to enable this feature.
    </div>
    """, unsafe_allow_html=True)

# Don't check again - these variables are already defined at the top of the script
# Just show a notification based on their values
if not MONGODB_AVAILABLE or not OPENAI_AVAILABLE:
    # Add notification at the top of the app about optional MongoDB features
    st.sidebar.markdown("""
    <div style="padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: #f8f9fa; border-left: 3px solid #046A38;">
        <b>ℹ️ Optional Feature Unavailable</b><br>
        MongoDB geo-based recommendations are unavailable because the required packages are not installed.
        <code>pip install pymongo openai</code> to enable this feature.
    </div>
    """, unsafe_allow_html=True)

# Add travel form
st.markdown("## " + t("create_itinerary"))
st.markdown("### " + t("trip_details"))

with st.form(key="travel_form"):
    # Basic trip information
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input(t("origin"), "Delhi")
        destination = st.text_input(t("destination"), "Agra")
        preferences = st.text_input(t("preferences"), "Historical sites, Culture, Food")
    
    with col2:
        # Date selection
        today = datetime.today()
        start_date = st.date_input(t("travel_dates"), 
                                 value=today + timedelta(days=7),
                                 min_value=today)
        
        duration = st.number_input(t("duration"), min_value=1, max_value=30, value=3)
        end_date = start_date + timedelta(days=duration)
        
        budget = st.selectbox(t("budget"), ["Budget", "Mid-range", "Luxury"])
    
    # Special requirements, if any
    special_requirements = st.text_area(t("special_requirements"), "", height=100)
    
    # Submit form
    submitted = st.form_submit_button(t("submit"))

# Create a dictionary of user inputs for later use
user_input = {
    "origin": origin,
    "destination": destination,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "duration": duration,
    "preferences": preferences,
    "budget": budget,
    "special_requirements": special_requirements
}

# Save destination to session state
st.session_state.destination = destination  # Save destination to session_state

# Save user input to session state for later use in maps
st.session_state.user_input = user_input  # Save for later map usage

# Process form submission
if submitted:
    # Show the input summary
    st.markdown("### " + t("request_details"))
    input_summary = f"""
    - **{t('from')}:** {origin}
    - **{t('destination')}:** {destination}
    - **{t('when')}:** {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}
    - **{t('duration')}:** {duration} days
    - **{t('preferences')}:** {preferences}
    - **{t('budget')}:** {budget}
    """
    st.markdown(input_summary)
    
    # Original travel request prompt
    input_text = f"Origin: {origin}, Destination: {destination}, Travel dates: {start_date} to {end_date}, Duration: {duration} days, Preferences: {preferences}, Budget: {budget}"
    
    # Check if API key is available
    if 'gemini_api_key' not in st.session_state or not st.session_state.gemini_api_key:
        st.error("Please enter your Gemini API key in the sidebar to generate an itinerary.")
    else:
        # Process the travel request
        with st.spinner("Generating your personalized travel itinerary..."):
            try:
                # Check if Tailvy API is available
                if 'tailvy_api_key' in st.session_state and st.session_state.tailvy_api_key:
                    # Use Tailvy API for enhanced travel planning
                    st.info("Using Tailvy API for enhanced travel recommendations...")
                    
                    tailvy_response = use_tailvy_api(
                        input_text, 
                        st.session_state.tailvy_api_key,
                        endpoint="travel"
                    )
                    
                    if tailvy_response:
                        # If Tailvy API call was successful, use its results
                        try:
                            st.session_state.step_results["destination_research"] = tailvy_response.get("destination_info", "")
                            st.session_state.step_results["accommodation"] = tailvy_response.get("accommodations", "")
                            st.session_state.step_results["transportation"] = tailvy_response.get("transportation", "")
                            st.session_state.step_results["activities"] = tailvy_response.get("activities", "")
                            st.session_state.step_results["dining"] = tailvy_response.get("dining", "")
                            
                            # Generate final itinerary with Tailvy integration
                            st.session_state.generated_itinerary = tailvy_response.get("itinerary", "")
                            
                            # Set tailvy_used flag to True
                            st.session_state.tailvy_used = True
                            
                            # Success message
                            st.success("Your Tailvy-enhanced travel itinerary has been successfully generated!")
                            
                            # Switch to the itinerary tab
                            st.session_state.active_tab = "full_itinerary"
                            
                        except Exception as e:
                            st.warning(f"Error processing Tailvy data: {str(e)}. Falling back to default method.")
                            # If error in processing Tailvy data, fall back to the default method
                            tailvy_response = None
                            st.session_state.tailvy_used = False
                    
                # If Tailvy API not available or failed, use default method
                if 'tailvy_api_key' not in st.session_state or not st.session_state.tailvy_api_key or not tailvy_response:
                    # Reset tailvy_used flag since we're using the default method
                    st.session_state.tailvy_used = False
                    
                    # Step 1: Destination Research
                    with st.status("Researching destination..."):
                        st.session_state.step_results["destination_research"] = run_task(
                            destination_research_task, 
                            input_text, 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Step 2: Accommodation
                    with st.status("Finding accommodations..."):
                        st.session_state.step_results["accommodation"] = run_task(
                            accommodation_task, 
                            input_text, 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Step 3: Transportation
                    with st.status("Planning transportation..."):
                        st.session_state.step_results["transportation"] = run_task(
                            transportation_task, 
                            input_text, 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Step 4: Activities
                    with st.status("Discovering activities..."):
                        st.session_state.step_results["activities"] = run_task(
                            activities_task, 
                            input_text, 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Step 5: Dining
                    with st.status("Finding dining options..."):
                        st.session_state.step_results["dining"] = run_task(
                            dining_task, 
                            input_text, 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Step 6: Generate final itinerary
                    with st.status("Creating final itinerary..."):
                        # Combine results for the final itinerary
                        combined_results = f"""
                        Destination Research: {st.session_state.step_results['destination_research']}
                        
                        Accommodation: {st.session_state.step_results['accommodation']}
                        
                        Transportation: {st.session_state.step_results['transportation']}
                        
                        Activities: {st.session_state.step_results['activities']}
                        
                        Dining: {st.session_state.step_results['dining']}
                        """
                        
                        st.session_state.generated_itinerary = run_task(
                            itinerary_task, 
                            f"{input_text}\n\n{combined_results}", 
                            api_key=st.session_state.gemini_api_key
                        )
                    
                    # Success message
                    st.success("Your travel itinerary has been successfully generated!")
                    
                    # Switch to the itinerary tab
                    st.session_state.active_tab = "full_itinerary"
                
            except Exception as e:
                st.error(f"Error generating itinerary: {str(e)}")
                st.info("Please check your API key and try again. Make sure you're using a valid API key.")
else:
    # When form is not submitted yet, show a sample itinerary or instructions
    input_text = f"Origin: {origin}, Destination: {destination}, Travel dates: {start_date} to {end_date}, Duration: {duration} days, Preferences: {preferences}, Budget: {budget}"

# Create tabs for the interface (including chatbot)
tabs_list = [
    t("full_itinerary"), 
    t("details"), 
    t("download_share"), 
    "🗺️ " + t("map_view"), 
    "🤖 " + t("chat")
]

# Check if we should activate a specific tab
if 'active_tab' in st.session_state:
    active_tab_index = 0  # Default to first tab
    if st.session_state.active_tab == "full_itinerary":
        active_tab_index = 0
    elif st.session_state.active_tab == "details":
        active_tab_index = 1
    elif st.session_state.active_tab == "download_share":
        active_tab_index = 2
    elif st.session_state.active_tab == "map_view":
        active_tab_index = 3
    elif st.session_state.active_tab == "chat":
        active_tab_index = 4
    
    # Store active tab index
    st.session_state.active_tab_index = active_tab_index
    
tabs = st.tabs(tabs_list)

# Itinerary tab
with tabs[0]:
    if st.session_state.generated_itinerary:
        # Add Tailvy badge if Tailvy API was used
        if 'tailvy_api_key' in st.session_state and st.session_state.tailvy_api_key and 'tailvy_used' in st.session_state and st.session_state.tailvy_used:
            st.markdown(
                """
                <div style="display: inline-block; background-color: #046A38; color: white; 
                padding: 5px 10px; border-radius: 15px; margin-bottom: 10px; font-size: 0.8rem;">
                    ✨ Enhanced with Tailvy AI
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        st.markdown('<div class="output-container"><div class="output-text">' + 
                   st.session_state.generated_itinerary + '</div></div>', 
                   unsafe_allow_html=True)

# Details tab
with tabs[1]:
    if st.session_state.step_results.get("destination_research"):
        st.markdown('<div class="output-container"><h3>🧭 Destination Information</h3><div class="output-text">' + 
                    st.session_state.step_results["destination_research"] + '</div></div>', 
                    unsafe_allow_html=True)
    
    if st.session_state.step_results.get("dining"):
        st.markdown('<div class="output-container"><h3>🍽️ Dining Recommendations</h3><div class="output-text">' + 
                    st.session_state.step_results["dining"] + '</div></div>', 
                    unsafe_allow_html=True)

# Download and share tab
with tabs[2]:
    if st.session_state.generated_itinerary:
        st.markdown('<div class="output-container"><h3>' + t("save_itinerary") + '</h3>', unsafe_allow_html=True)
        # Get destination from session state or use a default value
        destination = st.session_state.get("destination", "Travel")
        download_link = get_download_link(st.session_state.generated_itinerary, f"Travel_Itinerary_{destination.replace(' ', '_')}.txt")
        st.markdown(download_link, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Maps and visualization tab
with tabs[3]:
    st.markdown('<h3 class="output-text">Destination Map</h3>', unsafe_allow_html=True)
    
    # Get destination value from session_state (default to "Delhi" if not available)
    destination = st.session_state.get("destination", "Delhi")
    
    # Add search options for MongoDB geo search if available
    mongo_results = None
    # Make sure to check the variables that are now guaranteed to be defined
    if MONGODB_AVAILABLE and OPENAI_AVAILABLE and st.session_state.get("mongodb_uri", "") and st.session_state.get("openai_api_key", ""):
        st.markdown('<div class="output-container">', unsafe_allow_html=True)
        st.markdown('<h4 class="output-text">Find Nearby Attractions</h4>', unsafe_allow_html=True)
        
        search_term = st.text_input("What would you like to find near your destination?", 
                                    placeholder="e.g., historical sites, restaurants, parks")
        
        radius = st.slider("Search radius (meters)", 1000, 20000, 5000, step=1000)
        
        if st.button("Search"):
            with st.spinner("Searching for nearby attractions..."):
                mongo_results = find_nearby_attractions(destination, search_term, radius)
                if mongo_results and mongo_results.get("count", 0) > 0:
                    st.session_state.mongodb_used = True
                    st.success(f"Found {mongo_results['count']} attractions near {destination}!")
                else:
                    st.warning(f"No attractions found for '{search_term}' near {destination}.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    # Simple UI message when MongoDB modules are available but not configured
    elif MONGODB_AVAILABLE and OPENAI_AVAILABLE:
        st.info("""
        ℹ️ **MongoDB Geo Search Available**
        
        You can enable location-based attraction search by adding:
        1. MongoDB Connection URI
        2. OpenAI API Key
        
        Configure these in the settings panel to search for attractions near your destination.
        """)
    # Clear message about package installation when modules aren't available
    else:
        st.info("""
        ℹ️ **MongoDB Geo Search (Optional Feature)**
        
        This feature requires additional packages:
        ```
        pip install pymongo openai
        ```
        
        After installation, restart the app to enable location-based attraction search.
        """)
    
    # Get latitude and longitude via geocoding
    try:
        geolocator = Nominatim(user_agent="travel_app")
        location = geolocator.geocode(destination)
        if location:
            lat, lon = location.latitude, location.longitude
        else:
            lat, lon = 28.6139, 77.2090  # Default to Delhi if location not found
    except:
        lat, lon = 28.6139, 77.2090  # Default to Delhi if error
    
    # Create map data (can dynamically generate data for attractions near destination if needed)
    if mongo_results and mongo_results["count"] > 0:
        # Create DataFrame for MongoDB results
        attractions = mongo_results["results"]
        map_data = pd.DataFrame([
            {
                'lat': att["location"]["coordinates"][1],
                'lon': att["location"]["coordinates"][0],
                'name': att.get("name", "Attraction"),
                'description': att.get("description", ""),
                'distance': att.get("distance", 0) / 1000  # Convert to km
            } for att in attractions
        ])
        
        # Add the destination point as well
        destination_point = pd.DataFrame({
            'lat': [lat],
            'lon': [lon],
            'name': [destination],
            'description': ["Your destination"],
            'distance': [0]
        })
        
        map_data = pd.concat([destination_point, map_data], ignore_index=True)
        
        # Display the attraction results in a table
        st.markdown('<div class="output-container">', unsafe_allow_html=True)
        st.markdown('<h4 class="output-text">Nearby Attractions</h4>', unsafe_allow_html=True)
        
        # Display the attractions with distances
        for i, row in map_data.iterrows():
            if i == 0:  # Skip the destination point in the listing
                continue
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; border-left: 3px solid #FF671F; background-color: #f8f9fa;">
                <strong>{row['name']}</strong> ({row['distance']:.2f} km away)<br>
                {row['description']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Just show the destination point
        map_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lon],
            'name': [destination]
        })
    
    # Display the map
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="output-text">Interactive Map</h4>', unsafe_allow_html=True)
    map_view = pdk.ViewState(latitude=lat, longitude=lon, zoom=11, pitch=50)
    
    # Create layers for the map
    if mongo_results and mongo_results["count"] > 0:
        # Create text layer for labels
        text_layer = pdk.Layer(
            'TextLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_text='name',
            get_size=16,
            get_color=[0, 0, 0, 200],
            get_angle=0,
            get_text_anchor='"middle"',
            get_alignment_baseline='"bottom"',
        )
        
        # Create scatter layer with different colors for destination vs attractions
        scatter_layer = pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[index === 0 ? 255 : 4, index === 0 ? 103 : 106, index === 0 ? 31 : 56, 200]',
            get_radius='index === 0 ? 1000 : 500',
            pickable=True,
        )
        
        # Render the map with both layers
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            initial_view_state=map_view,
            layers=[scatter_layer, text_layer],
            tooltip={"text": "{name}\n{description}"}
        ))
    else:
        # Just create a simple scatter layer for the destination
        scatter_layer = pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[255, 103, 31, 200]',  # Saffron color with transparency
            get_radius=1000,
        )
        
        # Render the map
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            initial_view_state=map_view,
            layers=[scatter_layer],
        ))
    st.markdown('</div>', unsafe_allow_html=True)

# Chatbot interface tab (Clear button removed)
with tabs[4]:
    st.markdown('<h3 class="output-text">AI Travel Assistant</h3>', unsafe_allow_html=True)
    
    # Display MCP badge if connected
    if MCP_AVAILABLE and st.session_state.get("mcp_connected", False):
        st.markdown(
            """
            <div style="display: inline-block; background-color: #3366cc; color: white; 
            padding: 5px 10px; border-radius: 15px; margin-bottom: 10px; font-size: 0.8rem;">
                🧠 Enhanced with Model Context Protocol
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Store conversation history in session state (message, sender, timestamp)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # User input field and send button
    user_question = st.text_input("Ask a question about your travel plans:", key="user_question")
    
    # Check if API key is available
    if user_question and user_question.strip():
        if 'gemini_api_key' not in st.session_state or not st.session_state.gemini_api_key:
            st.error("Please enter your Gemini API key in the sidebar to use the chat feature.")
        else:
            # Create context for the chatbot
            if "user_input" in st.session_state:
                context = f"Travel Plan: {st.session_state.user_input}\nQuestion: {user_question}"
            else:
                context = f"Question: {user_question}"
            
            # Try using MCP first if available and configured
            mcp_response = None
            mcp_used = False
            if MCP_AVAILABLE and st.session_state.get("mcp_connected", False):
                with st.spinner("Getting MCP response..."):
                    mcp_response = get_chatbot_response_with_mcp(user_question, context)
                    if mcp_response:
                        mcp_used = True
            
            # Try using Tailvy API if MCP not available or failed
            tailvy_response = None
            tailvy_used = False
            if not mcp_used and 'tailvy_api_key' in st.session_state and st.session_state.tailvy_api_key:
                try:
                    tailvy_response = use_tailvy_api(
                        user_question, 
                        st.session_state.tailvy_api_key,
                        endpoint="chat"
                    )
                    if tailvy_response:
                        tailvy_used = True
                except:
                    tailvy_response = None
            
            # Generate response and add to conversation history
            with st.spinner("Thinking..."):
                try:
                    with st.progress(0) as progress_bar:
                        for i in range(100):
                            # Simulating progress
                            progress_bar.progress(i + 1)
                            if i < 98:  # Add a small delay for the visual effect
                                import time
                                time.sleep(0.01)
                    
                    # Use responses in order of preference: MCP → Tailvy → Gemini
                    if mcp_used and mcp_response:
                        response = mcp_response
                        # Mark that MCP was used
                        st.session_state.mcp_used = True
                        st.session_state.tailvy_used = False
                    elif tailvy_used and tailvy_response:
                        response = tailvy_response.get("response", "I couldn't find an answer to that question.")
                        # Mark that Tailvy was used
                        st.session_state.mcp_used = False
                        st.session_state.tailvy_used = True
                    else:
                        response = run_task(chatbot_task, context, api_key=st.session_state.gemini_api_key)
                        # Reset usage flags
                        st.session_state.mcp_used = False
                        st.session_state.tailvy_used = False
                    
                    now = datetime.now().strftime("%H:%M")
                    st.session_state.messages.append({"text": user_question, "sender": "user", "time": now})
                    st.session_state.messages.append({"text": response, "sender": "ai", "time": now})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Please check your connections and try again.")
    
    # Display conversation history (with badges for response sources)
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(reversed(st.session_state.messages)):
            is_user = message["sender"] == "user"
            message_class = "user-message" if is_user else "ai-message"
            
            # Add source badge for AI messages
            source_badge = ""
            if not is_user and idx > 0:  # Only for AI messages and when we have message pairs
                if st.session_state.get("mcp_used", False) and (idx % 2 == 1):  # Check if this message pair used MCP
                    source_badge = '<span style="background-color: #3366cc; color: white; border-radius: 10px; padding: 2px 5px; font-size: 0.7rem; margin-left: 5px;">MCP</span>'
                elif st.session_state.get("tailvy_used", False) and (idx % 2 == 1):  # Check if this message pair used Tailvy
                    source_badge = '<span style="background-color: #046A38; color: white; border-radius: 10px; padding: 2px 5px; font-size: 0.7rem; margin-left: 5px;">Tailvy</span>'
            
            st.markdown(
                f"""<div style="display: flex; justify-content: {'flex-end' if is_user else 'flex-start'}; margin-bottom: 10px;">
                    <div class="{message_class}" style="border-radius: 10px; padding: 10px; max-width: 80%;">
                        <div style="font-size: 0.8rem; color: #888; margin-bottom: 5px;">{message["sender"].upper()} {source_badge} - {message["time"]}</div>
                        <div class="output-text">{message["text"]}</div>
                    </div>
                </div>""",
                unsafe_allow_html=True
            )

st.markdown("""
<div style="margin-top: 50px; text-align: center; padding: 20px; color: #6c757d; font-size: 0.8rem;">
    <p>""" + t("built_with") + """</p>
    <p style="margin-top: 10px;">Created by TechMatrix Solvers for <a href="https://www.hackbyte.in/" target="_blank">IIITDMJ HackByte3.0</a> (April 2025)</p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px;">
        <a href="https://www.linkedin.com/in/abhay-gupta-197b17264/" target="_blank" style="color: #0077B5;">Abhay</a>
        <a href="https://www.linkedin.com/in/jay-kumar-jk/" target="_blank" style="color: #0077B5;">Jay</a>
        <a href="https://www.linkedin.com/in/kripanshu-gupta-a66349261/" target="_blank" style="color: #0077B5;">Kripanshu</a>
        <a href="https://www.linkedin.com/in/aditi-soni-259813285/" target="_blank" style="color: #0077B5;">Aditi</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Add helper function for MCP connection
def test_mcp_connection(server_url):
    """
    Test connection to MCP server
    
    Args:
        server_url (str): WebSocket URL for the MCP server
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    if not MCP_AVAILABLE:
        return False
        
    try:
        # Create async function to test connection
        async def test_connection():
            try:
                # Set up server parameters
                server_params = WebSocketServerParameters(url=server_url)
                
                # Attempt connection with timeout
                client = ClientSession.create(server_params)
                await asyncio.wait_for(client.initialize(), timeout=5.0)
                
                # If we get here, connection was successful
                await client.close()
                return True
            except Exception as e:
                print(f"MCP connection error: {str(e)}")
                return False
                
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_connection())
        loop.close()
        return result
    except Exception as e:
        print(f"Error testing MCP connection: {str(e)}")
        return False

# Add function to use MCP for chatbot responses when available
def get_chatbot_response_with_mcp(question, context=None):
    """
    Get a chatbot response using MCP if available
    
    Args:
        question (str): User question
        context (str): Additional context
        
    Returns:
        str: AI response
    """
    if not MCP_AVAILABLE or not st.session_state.get("mcp_connected", False):
        # Fall back to regular method if MCP not available or not connected
        return None
        
    try:
        # Create async function to get response
        async def get_response():
            try:
                # Connect to MCP server
                server_params = WebSocketServerParameters(url=st.session_state.mcp_server_url)
                async with ClientSession.create(server_params) as client:
                    # Initialize connection
                    await client.initialize()
                    
                    # List available tools
                    tools = await client.list_tools()
                    
                    # Look for travel-related tools
                    travel_tool = next((t for t in tools if "travel" in t.name.lower()), None)
                    
                    if travel_tool:
                        # Call the travel tool with our question
                        result = await client.call_tool(
                            travel_tool.name,
                            arguments={
                                "question": question,
                                "context": context or ""
                            }
                        )
                        return result
                    else:
                        # If no specific travel tool, call a generic "echo" or similar tool
                        # This is a fallback if the MCP server doesn't have travel-specific tools
                        generic_tool = next((t for t in tools if "echo" in t.name.lower() or "chat" in t.name.lower()), None)
                        if generic_tool:
                            result = await client.call_tool(
                                generic_tool.name,
                                arguments={"message": f"Travel question: {question} Context: {context or ''}"}
                            )
                            return result
                        
                        # No suitable tools found
                        return None
            except Exception as e:
                print(f"MCP response error: {str(e)}")
                return None
                
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_response())
        loop.close()
        return result
    except Exception as e:
        print(f"Error getting MCP response: {str(e)}")
        return None

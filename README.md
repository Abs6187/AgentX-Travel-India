---
title: AgentX-Travel India
emoji: 🏃
colorFrom: orange
colorTo: green
sdk: streamlit
sdk_version: 1.42.2
app_file: app.py
pinned: false
short_description: LLM + Langchain Travel Planner for India
---
<p align="center">
  <img src="android-chrome-512x512.png" alt="AgentX Logo" width="150"/>
</p>
# AgentX Travel India v0

A smart travel itinerary planner built by TechMatrix Solvers for IIITDMJ HackByte3.0. This application leverages AI to create personalized travel itineraries for destinations across India.

## 🚀 Deployment

This application is deployed on Hugging Face Spaces:
- [AgentX-Travel-India](https://huggingface.co/spaces/Abs6187/AgentX-Travel-India) - Latest version
- [AgentX-Travel-India_v01](https://huggingface.co/spaces/Abs6187/AgentX-Travel-India_v01) - Development version

## Tracks Followed in Hackathon HackByte 3.0:
1. Gemini API
2. MongoDB Atlas API
3. Cloudflare AI SDK/ HuggingFace
4. Github
5. Postman testing

![Tracks_Followed_HackByte3_0](Tracks_followed_HackByte3.png)

##  Features

- **AI-Powered Itinerary Generation**: Create detailed day-by-day travel plans customized to your preferences
- **Multi-Agent System**: Specialized AI agents for research, accommodation, transportation, activities, dining, and itinerary integration
- **Optional Enhanced Recommendations**: Integration with optional Tailvy API and MongoDB for improved suggestions
- **Interactive Maps**: Visualize your travel destinations with integrated mapping
- **Geo-based Attraction Search**: Find nearby attractions using MongoDB's geospatial and vector search (optional)
- **Chatbot Assistant**: Get answers to your travel questions through our conversational AI
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Downloadable Itineraries**: Save your travel plans offline for easy access

##  Getting Started

### Prerequisites
- Python 3.8+
- Google API Key (for Gemini access)
- (Optional) Tailvy API Key for enhanced travel recommendations
- (Optional) MongoDB Atlas account and OpenAI API Key for geo-based attraction search

### Installation

```bash
# Clone the repository
git clone https://github.com/Abs6187/agentx-travel-india.git
cd agentx-travel-india

# Install dependencies
pip install -r requirements.txt

# Optional: Install MongoDB and OpenAI for geo-based recommendations
pip install pymongo openai

# Set up environment variables (optional)
export GEMINI_API_KEY="your_api_key_here"

# Run the application
streamlit run app.py
```

## 💻 Usage

1. Enter your Google Gemini API key in the settings panel
2. (Optional) Add Tailvy API key for enhanced recommendations
3. (Optional) Configure MongoDB and OpenAI for geo-based attraction search
4. Enter your origin, destination, and travel details
5. Specify your preferences and budget
6. Click "Create My Personal Travel Itinerary"
7. Review the generated itinerary
8. Explore nearby attractions on the map tab

## 🔑 API Key Setup

You can set up your API keys through the app's settings panel:

1. **Required**: Google Gemini API Key - Get from https://ai.google.dev/
2. **Optional**: Tailvy API Key - For enhanced travel recommendations
3. **Optional**: MongoDB Connection URI - For geo-based attraction search
4. **Optional**: OpenAI API Key - For vector search of attractions

## 🗺️ MongoDB Integration

The app includes optional MongoDB integration for geo-based attraction recommendations:

1. Stores attraction data with geographical coordinates
2. Uses MongoDB's geospatial queries to find attractions near your destination
3. Implements vector search using OpenAI embeddings for semantic matching
4. Visualizes attractions on an interactive map

If you have a MongoDB Atlas account, you can:
- Enter your connection URI in the settings
- Provide an OpenAI API key for vector embeddings
- Initialize a sample dataset with Indian attractions
- Search for attractions near your destination based on your interests

## 📊 Architecture Evolution

Our project architecture has evolved through multiple versions:

### Initial Architecture (v0)
![Architecture v0](Architecture_of_travel_planner_v0.png)
*Initial design with basic AI agent integration*

### Hackathon Implementation (v0.1)
![Architecture v0.1](Architecture_of_travel_planner_v0.1.png)
*Enhanced architecture implemented during the hackathon with improved agent communication*

### Advanced Implementation (v1)
![Architecture v1](Architecture_of_travel_planner_v1.png)
*Advanced version with additional data sources and optimized workflows*

### Future Vision (v2) - Beyond Hackathon Scope
![Architecture v2](Architecture_of_travel_planner_v2.png)
*Planned future architecture with expanded capabilities and integrations*

## 📊 Current Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                         (Streamlit)                             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Orchestration Layer                        │
└───┬───────┬───────┬───────┬───────┬───────┬───────┬─────────────┘
    │       │       │       │       │       │       │
    ▼       ▼       ▼       ▼       ▼       ▼       ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Research │ │Accomm.  │ │Transport│ │Activities│ │ Dining  │ │Itinerary│ │ Chatbot │
│  Agent  │ │ Agent   │ │ Agent   │ │  Agent   │ │ Agent   │ │ Agent   │ │  Agent  │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │           │           │           │
     └───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
                                        │
                                        ▼
┌────────────────┬────────────────┬─────────────────┬───────────────┐
│ Google Gemini  │  Tailvy API    │  MongoDB Atlas  │  OpenAI API   │
│   (Required)   │  (Optional)    │   (Optional)    │  (Optional)   │
└────────────────┴────────────────┴─────────────────┴───────────────┘
```

The application follows a multi-agent architecture where specialized AI agents handle different aspects of travel planning. These agents work collaboratively to create a comprehensive travel itinerary tailored to the user's preferences.

## 👥 Team Members

This project was created by TechMatrix Solvers for IIITDMJ HackByte3.0 (April 4-6, 2024):

- **Team Leader**: Abhay Gupta ([LinkedIn](https://www.linkedin.com/in/abhay-gupta-197b17264/))
- Jay Kumar ([LinkedIn](https://www.linkedin.com/in/jay-kumar-jk/))
- Kripanshu Gupta ([LinkedIn](https://www.linkedin.com/in/kripanshu-gupta-a66349261/))
- Aditi Soni ([LinkedIn](https://www.linkedin.com/in/aditi-soni-259813285/))

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.32.2
- **AI Framework**: LangChain with Google Genai 0.0.10
- **Language Model**: Google Generative AI (Gemini) 0.3.2
- **Geolocation**: Geopy 2.4.1
- **Visualization**: Pydeck 0.8.0
- **Data Processing**: Pandas 2.1.4
- **Optional**: MongoDB for geo-based recommendations
- **Optional**: OpenAI for vector embeddings
- **Optional**: Tailvy API for enhanced travel planning

## WATCH THE VIDEO
[![Watch the video](https://img.youtube.com/vi/1l1WXob-diM/0.jpg)](https://www.youtube.com/watch?v=1l1WXob-diM)



## 🙏 Acknowledgements

- [HackByte](https://www.hackbyte.in/) for hosting this hackathon
- IIITDM Jabalpur for providing the venue and support
- MongoDB for the geo-spatial and vector search capabilities
- The open-source community for the incredible tools that made this project possible

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

"""
# travel.py - AI Agent System for Travel Planning
# ----------------------------------------------
#
# This module implements a sophisticated multi-agent system for travel planning
# with a specific focus on Indian travel destinations and experiences.
#
# ARCHITECTURE:
# The system uses a collection of specialized AI agents, each responsible for
# a different aspect of travel planning:
#
# 1. Destination Research Agent - Researches destinations based on user preferences
# 2. Accommodation Agent - Suggests suitable accommodations meeting budget and preference constraints
# 3. Transportation Agent - Plans optimal transportation between locations
# 4. Activities Agent - Curates personalized activities based on interests
# 5. Dining Agent - Recommends dining experiences showcasing local cuisine
# 6. Itinerary Agent - Compiles all recommendations into a cohesive day-by-day plan
# 7. Chatbot Agent - Provides conversational responses to travel queries
#
# Each agent is powered by Google's Generative AI (Gemini) and is specialized through
# careful system prompting that defines its role, goals, and expected outputs.
#
# WORKFLOW:
# 1. User submits travel preferences
# 2. Each agent processes the information in sequence
# 3. Final itinerary is compiled from all agent outputs
# 4. Results are presented to the user as a complete travel plan
#
# PRIMARY FUNCTIONS:
# - run_task(): Core function to execute a specific agent task
# - generate_travel_itinerary(): Orchestrates the full planning process
# - save_itinerary_to_file(): Saves the generated itinerary for the user
#
# Created by TechMatrix Solvers for IIITDMJ HackByte3.0
"""

import os
import json
import logging
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------------------------------------------------------------------
# Agent and Task Classes with Type Hints and Docstrings
# -------------------------------------------------------------------------------
class Agent:
    def __init__(self, role: str, goal: str, backstory: str, personality: str = "", llm=None) -> None:
        """
        Initialize an Agent with role, goal, backstory, personality, and assigned LLM.
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.personality = personality
        self.tools = []  # Initialize with empty list for future tool integrations
        self.llm = llm

class Task:
    def __init__(self, description: str, agent: Agent, expected_output: str, context=None) -> None:
        """
        Initialize a Task with its description, the responsible agent, expected output, and optional context.
        """
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.context = context or []

# -------------------------------------------------------------------------------
# Initialize LLM
# -------------------------------------------------------------------------------
def initialize_llm(api_key=None):
    """Initialize the LLM with the provided API key or from environment variables.
    
    Args:
        api_key (str, optional): API key for Google Generative AI. 
            If None, will try to get from environment variables.
            
    Returns:
        ChatGoogleGenerativeAI or None: Initialized LLM instance or None if initialization failed.
    """
    # First try the provided API key
    if api_key:
        google_api_key = api_key
    else:
        # Fall back to environment variable
        google_api_key = os.getenv("GEMINI_API_KEY")
    
    if not google_api_key:
        logging.warning("GEMINI_API_KEY is not set. AI functionality will be limited.")
        return None
    
    # Basic API key format validation
    if not google_api_key.startswith("AI"):
        logging.warning("API key format appears incorrect. Should start with 'AI'.")
    
    try:
        # Attempt to initialize the LLM
        llm_instance = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", 
            google_api_key=google_api_key,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192
        )
        logging.info("LLM initialized successfully.")
        return llm_instance
    except Exception as e:
        logging.error(f"Error initializing LLM: {e}")
        # More detailed error message for common issues
        if "403" in str(e) or "401" in str(e):
            logging.error("Authentication error: Your API key may be invalid or expired.")
        elif "429" in str(e):
            logging.error("Rate limit exceeded: Too many requests to the API.")
        elif "timeout" in str(e).lower():
            logging.error("Request timed out: Network issue or service unavailability.")
        return None

# Initialize with environment variable for now
llm = initialize_llm()

# -------------------------------------------------------------------------------
# Define Travel Agents
# -------------------------------------------------------------------------------
destination_research_agent = Agent(
    role="Destination Research Agent",
    goal=(
        "Research and provide comprehensive information about the destination including popular attractions, "
        "local culture, weather patterns, best times to visit, and local transportation options with special focus on Indian context."
    ),
    backstory=(
        "An experienced travel researcher with extensive knowledge of Indian destinations. "
        "I specialize in uncovering both popular attractions and hidden gems that match travelers' interests."
    ),
    personality="Curious, detail-oriented, and knowledgeable about Indian cultures and travel trends.",
    llm=llm,
)

accommodation_agent = Agent(
    role="Accommodation Agent",
    goal="Find and recommend suitable accommodations based on the traveler's preferences, budget, and location requirements with focus on Indian hospitality options.",
    backstory="A hospitality expert who understands different types of accommodations in India and can match travelers with their ideal places to stay.",
    personality="Attentive, resourceful, and focused on comfort and value.",
    llm=llm,
)

transportation_agent = Agent(
    role="Transportation Agent",
    goal="Plan efficient transportation between the origin, destination, and all points of interest in the itinerary using Indian transportation networks.",
    backstory="A logistics specialist with knowledge of India's transportation systems, from flights to local transit options including trains, buses, and auto-rickshaws.",
    personality="Efficient, practical, and detail-oriented.",
    llm=llm,
)

activities_agent = Agent(
    role="Activities & Attractions Agent",
    goal="Curate personalized activities and attractions that align with the traveler's interests, preferences, and time constraints in Indian destinations.",
    backstory="An enthusiastic explorer who has experienced diverse activities across India and knows how to match experiences to individual preferences.",
    personality="Enthusiastic, creative, and personable.",
    llm=llm,
)

dining_agent = Agent(
    role="Dining & Culinary Agent",
    goal="Recommend dining experiences that showcase local Indian cuisine while accommodating dietary preferences and budget considerations.",
    backstory="A culinary expert with knowledge of India's diverse food scenes and an appreciation for authentic local dining experiences.",
    personality="Passionate about food, culturally aware, and attentive to preferences.",
    llm=llm,
)

itinerary_agent = Agent(
    role="Itinerary Integration Agent",
    goal="Compile all recommendations into a cohesive, day-by-day itinerary that optimizes time, minimizes travel fatigue, and maximizes enjoyment for travel in India.",
    backstory="A master travel planner who understands how to balance activities, rest, and logistics to create the perfect Indian travel experience.",
    personality="Organized, balanced, and practical.",
    llm=llm,
)

# -------------------------------------------------------------------------------
# Define Chatbot Agent and Task for Interactive Conversation
# -------------------------------------------------------------------------------
chatbot_agent = Agent(
    role="Chatbot Agent",
    goal="Engage in interactive conversation to answer travel-related queries about India.",
    backstory="A conversational AI assistant who provides instant, accurate travel information and recommendations for Indian destinations.",
    personality="Friendly, conversational, and knowledgeable about travel in India.",
    llm=llm,
)

chatbot_task = Task(
    description="Provide a conversational and detailed response to travel-related queries about Indian destinations.",
    agent=chatbot_agent,
    expected_output="A friendly, helpful response to the user's query about travel in India."
)

# -------------------------------------------------------------------------------
# Define Other Travel Tasks
# -------------------------------------------------------------------------------
destination_research_task = Task(
    description="""Research {destination} thoroughly, considering the traveler's interests in {preferences}.
    
Efficient research parameters:
- Prioritize research in these critical categories:
    * Top attractions that match specific {preferences} (not generic lists)
    * Local transportation systems with cost-efficiency analysis
    * Neighborhood breakdown with accommodation recommendations by budget tier
    * Seasonal considerations for the specific travel dates
    * Safety assessment with specific areas to embrace or avoid
    * Cultural norms that impact visitor experience (dress codes, tipping, etiquette)
    
- Apply efficiency filters:
    * Focus exclusively on verified information from official tourism boards, recent travel guides, and reliable local sources
    * Analyze recent visitor reviews (< 6 months old) to identify changing conditions
    * Evaluate price-to-experience value for attractions instead of just popularity
    * Identify logistical clusters where multiple interests can be satisfied efficiently
    * Research off-peak times for popular attractions to minimize waiting
    * Evaluate digital tools (apps, passes, reservation systems) that streamline the visit
    
- Create practical knowledge matrices:
    * Transportation method comparison (cost vs. time vs. convenience)
    * Weather impact on specific activities
    * Budget allocation recommendations based on preference priorities
    * Time-saving opportunity identification""",
    agent=destination_research_agent,
    expected_output="""Targeted destination brief containing:
1. Executive summary highlighting the 5 most relevant aspects based on {preferences}
2. Neighborhood analysis with accommodation recommendations mapped to specific interests
3. Transportation efficiency guide with cost/convenience matrix
4. Cultural briefing focusing only on need-to-know information that impacts daily activities
5. Seasonal advantages and challenges specific to travel dates
6. Digital resource toolkit (essential apps, websites, reservation systems)
7. Budget optimization strategies with price ranges for key experiences
8. Safety and health quick-reference including emergency contacts
9. Logistics efficiency map showing optimal activity clustering
10. Local insider advantage recommendations that save time or money

Format should prioritize scannable information with bullet points, comparison tables, and decision matrices rather than lengthy prose."""
)

accommodation_task = Task(
    description="Find suitable accommodations in {destination} based on a {budget} budget and preferences for {preferences}. Focus on Indian accommodations including heritage hotels, homestays, and modern options.",
    agent=accommodation_agent,
    expected_output="List of recommended accommodations with details on location, amenities, price range, and availability."
)

transportation_task = Task(
    description="Plan transportation from {origin} to {destination} and local transportation options during the stay. Include Indian railways, local buses, metro systems, and ride-hailing services where available.",
    agent=transportation_agent,
    expected_output="Transportation plan including flights/routes to the destination and recommendations for getting around locally."
)

activities_task = Task(
    description="""Suggest activities and attractions in {destination} that align with interests in {preferences}.
    
Detailed requirements:
- Categorize activities into: Cultural Experiences, Outdoor Adventures, Culinary Experiences, 
  Entertainment & Nightlife, Family-Friendly Activities, and Local Hidden Gems
- For each activity, include:
    * Detailed description with historical/cultural context where relevant
    * Precise location with neighborhood information
    * Operating hours with seasonal variations noted
    * Pricing information with different ticket options/packages
    * Accessibility considerations for travelers with mobility limitations
    * Recommended duration for the activity (minimum and ideal time)
    * Best time of day/week/year to visit
    * Crowd levels by season
    * Photography opportunities and restrictions
    * Required reservations or booking windows
- Include a mix of iconic must-see attractions and off-the-beaten-path experiences
- Consider weather patterns in {destination} during travel period
- Analyze the {preferences} to match specific personality types and interest levels
- Include at least 2-3 rainy day alternatives for outdoor activities
- Provide local transportation options to reach each attraction
- Note authentic local experiences that provide cultural immersion
- Flag any activities requiring special equipment, permits, or physical fitness levels""",
    agent=activities_agent,
    expected_output="""Comprehensive curated list of activities and attractions with:
1. Clear categorization by type (cultural, outdoor, culinary, entertainment, family-friendly, hidden gems)
2. Essential details for planning (location, timing, cost, requirements)
3. Special recommendations based on {preferences} with personalized suggestions
4. Weather contingency options
5. Insider tips for maximizing experience value
6. Logistical guidance for efficient navigation between attractions"""
)

dining_task = Task(
    description="""Recommend dining options in {destination} that showcase local cuisine while accommodating {preferences} with special attention to authentic Indian culinary experiences.
    
For each recommended dining establishment, provide:
- Name, location, and cuisine type
- Signature dishes and culinary specialties
- Price range and value assessment
- Ambiance description and dress code if applicable
- Operating hours and reservation policies
- Local popularity vs. tourist popularity
- Special dietary accommodations (vegetarian, vegan, gluten-free, etc.)
- Authentic cultural dining experiences that provide insight into local life""",
    agent=dining_agent,
    expected_output="""Curated dining guide for {destination} with:
1. Top restaurant recommendations categorized by meal type, cuisine, and price point
2. Must-try local dishes specific to the region
3. Unique dining experiences that reflect local culture
4. Budget-friendly options with exceptional value
5. Strategic meal timing to complement activity schedule
6. Advance reservation requirements where applicable
7. Special dietary consideration options
8. Hidden gems frequented by locals"""
)

itinerary_task = Task(
    description="""Create a day-by-day itinerary for a {duration}-day trip to {destination} based on all previous research and recommendations. Focus on authentic experiences that reflect true Indian culture and heritage.
    
The itinerary should:
- Balance activities with rest and travel time
- Group attractions by geographic proximity to minimize transit time
- Consider opening hours, best times to visit, and seasonal factors
- Include meal recommendations that complement the day's activities
- Provide contingency options for weather or unexpected closures
- Balance must-see attractions with authentic local experiences
- Account for {preferences} in prioritizing experiences
- Include precise timing, transportation methods, and logistical details
- Optimize for the traveler's interests while maintaining a realistic pace
- Incorporate free time for exploration and spontaneity""",
    agent=itinerary_agent,
    expected_output="""Complete day-by-day itinerary containing:
1. Daily schedule with timing, locations, and activities
2. Transportation details between all points
3. Meal recommendations with timing and cuisine type
4. Activity duration estimates with buffer time included
5. Alternative options for flexibility
6. Booking/reservation requirements with deadlines
7. Cost estimates for budgeting purposes
8. Local cultural insights for each experience
9. Strategic planning notes (best photo spots, crowd avoidance, etc.)
10. Evening entertainment options

Format should be scannable with clear headings, timing, and logistical details for easy reference during travel."""
)

# -------------------------------------------------------------------------------
# Helper Function to Run a Task with Full Agent & Task Information
# -------------------------------------------------------------------------------
def run_task(task: Task, input_text: str, api_key=None) -> str:
    """
    Run an agent task with the given input text and API key.
    
    Args:
        task: The Task to run
        input_text: User input text
        api_key: Optional Gemini API key to use
        
    Returns:
        str: The generated response or error message
    """
    # Check if we need to initialize or reinitialize the LLM
    current_llm = initialize_llm(api_key)
    if current_llm:
        # Update the agent's LLM
        task.agent.llm = current_llm
    elif not task.agent.llm:
        logging.error("No valid API key provided")
        return "⚠️ API Key Error: Please enter a valid Gemini API key in the settings to access AI features."
    
    # Prepare the system prompt
    system_prompt = f"""
    # Role: {task.agent.role}
    # Goal: {task.agent.goal}
    # Backstory: {task.agent.backstory}
    
    Instructions for output:
    {task.expected_output}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]
    
    try:
        # Start tracking time for possible timeout issues
        start_time = datetime.now()
        
        # Make the API call with timeout handling
        response = task.agent.llm.invoke(messages).content
        
        # Calculate response time for logging
        response_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"Task '{task.description[:30]}...' completed in {response_time:.2f} seconds")
        
        return response
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error running task: {error_msg}")
        
        # Create user-friendly error messages based on the exception
        if "timeout" in error_msg.lower():
            return "⚠️ Request timed out. The service might be experiencing high traffic. Please try again later."
        elif "429" in error_msg:
            return "⚠️ Rate limit exceeded. Please try again in a few minutes."
        elif "403" in error_msg or "401" in error_msg or "authentication" in error_msg.lower():
            return "⚠️ API Key Error: Your API key appears to be invalid or has expired. Please update it in settings."
        elif "quota" in error_msg.lower():
            return "⚠️ API quota exceeded. Your Gemini API key has reached its usage limit."
        else:
            # Generic error message for other types of errors
            return f"⚠️ Error processing your request. Please try again or check your API key settings."

# -------------------------------------------------------------------------------
# User Input Functions
# -------------------------------------------------------------------------------
def get_user_input() -> dict:
    """
    Collects user input for travel itinerary generation.
    """
    print("\n=== Travel Itinerary Generator ===\n")
    origin = input("Enter your origin: ")
    destination = input("Enter your destination: ")
    duration = input("Enter duration in days: ")
    
    current_date = datetime.now()
    start_date = current_date + timedelta(days=7)
    end_date = start_date + timedelta(days=int(duration))
    
    preferences = input("Enter your preferences (comma separated): ")
    budget = input("Enter your budget: ")
    
    return {
        "origin": origin,
        "destination": destination,
        "duration": duration,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "preferences": preferences,
        "budget": budget
    }

# -------------------------------------------------------------------------------
# Main Function to Generate Travel Itinerary
# -------------------------------------------------------------------------------
def generate_travel_itinerary(user_input: dict) -> str:
    """
    Generates a personalized travel itinerary by sequentially running defined tasks.
    """
    print("\nGenerating your personalized travel itinerary...\n")
    
    # Create input context using f-string formatting
    input_context = (
        f"Travel Request Details:\n"
        f"Origin: {user_input['origin']}\n"
        f"Destination: {user_input['destination']}\n"
        f"Duration: {user_input['duration']} days\n"
        f"Budget Level: {user_input['budget']}\n"
        f"Preferences/Interests: {user_input['preferences']}\n"
        f"Special Requirements: {user_input['special_requirements']}\n"
    )
    
    # Step 1: Destination Research
    print("Researching your destination...")
    destination_info = run_task(destination_research_task, input_context)
    print("✓ Destination research completed")
    
    # Step 2: Accommodation Recommendations
    print("Finding ideal accommodations...")
    accommodation_info = run_task(accommodation_task, input_context)
    print("✓ Accommodation recommendations completed")
    
    # Step 3: Transportation Planning
    print("Planning transportation...")
    transportation_info = run_task(transportation_task, input_context)
    print("✓ Transportation planning completed")
    
    # Step 4: Activities & Attractions
    print("Curating activities and attractions...")
    activities_info = run_task(activities_task, input_context)
    print("✓ Activities and attractions curated")
    
    # Step 5: Dining Recommendations
    print("Finding dining experiences...")
    dining_info = run_task(dining_task, input_context)
    print("✓ Dining recommendations completed")
    
    # Step 6: Create Day-by-Day Itinerary
    print("Creating your day-by-day itinerary...")
    combined_info = (
        input_context + "\n"
        "Destination Information:\n" + destination_info + "\n"
        "Accommodation Options:\n" + accommodation_info + "\n"
        "Transportation Plan:\n" + transportation_info + "\n"
        "Recommended Activities:\n" + activities_info + "\n"
        "Dining Recommendations:\n" + dining_info + "\n"
    )
    itinerary = run_task(itinerary_task, combined_info)
    print("✓ Itinerary creation completed")
    print("✓ Itinerary generation completed")
    
    return itinerary

# -------------------------------------------------------------------------------
# Save Itinerary to File
# -------------------------------------------------------------------------------
def save_itinerary_to_file(itinerary: str, user_input: dict, output_dir: str = None) -> str:
    """
    Saves the generated itinerary to a text file and returns the filepath.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"India_Travel_Itinerary_{user_input['destination']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    if output_dir:
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                logging.info(f"Created output directory: {output_dir}")
            except Exception as e:
                logging.error(f"Error creating directory {output_dir}: {e}")
                return ""
        filepath = os.path.join(output_dir, filename)
    else:
        filepath = filename
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(itinerary)
        logging.info(f"Your itinerary has been saved as: {filepath}")
        return filepath
    except Exception as e:
        logging.error(f"Error saving itinerary: {e}")
        return ""

# -------------------------------------------------------------------------------
# Main Function
# -------------------------------------------------------------------------------
def main() -> None:
    """
    Main entry point for the travel itinerary generator application.
    """
    print("Welcome to the India Travel Planner! Let's create your perfect itinerary.")
    user_input = get_user_input()
    
    print("\nGenerating your personalized travel itinerary...\n")
    itinerary = generate_travel_itinerary(user_input)
    
    print("\n" + "=" * 50)
    print("Your travel itinerary is ready!")
    print("=" * 50 + "\n")
    
    print(itinerary)
    
    output_file = save_itinerary_to_file(itinerary, user_input)
    print(f"\nYour itinerary has been saved to: {output_file}")

if __name__ == "__main__":
    main()

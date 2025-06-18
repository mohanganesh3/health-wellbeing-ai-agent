
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from langchain import hub
from langchain.memory import ConversationBufferMemory
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the Google Gemini model
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBuk9yz3u-oBcl3psgCXLs0bu4FSGPyFME'

try:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    print("✅ Gemini API connected successfully")
except Exception as e:
    print(f"❌ Error connecting to Gemini API: {e}")

# Initialize tools
search_tool = DuckDuckGoSearchRun()

# Health and Fitness specific tools
def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from weight in kg and height in cm"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return f"BMI: {bmi:.1f} ({category})"

def calculate_calories(age, weight, height, gender, activity_level):
    """Calculate recommended daily calories using Mifflin-St Jeor Equation"""
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    calories = bmr * activity_multipliers.get(activity_level.lower(), 1.2)
    return f"Recommended daily calories: {calories:.0f}"

# Mental health assessment tools
def assess_stress_level(stress_indicators):
    """Assess stress level based on indicators"""
    stress_keywords = ['overwhelmed', 'anxious', 'tired', 'sleepless', 'worried', 'pressure']
    stress_count = sum(1 for keyword in stress_keywords if keyword in stress_indicators.lower())
    
    if stress_count >= 4:
        return "High stress level detected. Consider relaxation techniques and professional support."
    elif stress_count >= 2:
        return "Moderate stress level. Practice mindfulness and stress management."
    else:
        return "Low stress level. Continue maintaining healthy habits."

def suggest_mental_wellness_activities(mood, energy_level):
    """Suggest activities based on mood and energy"""
    activities = {
        'low_energy': ['gentle breathing exercises', 'light stretching', 'meditation', 'journaling'],
        'moderate_energy': ['short walk', 'yoga', 'creative activities', 'reading'],
        'high_energy': ['exercise', 'dancing', 'outdoor activities', 'social activities']
    }
    
    energy_map = {
        'tired': 'low_energy',
        'low': 'low_energy',
        'okay': 'moderate_energy',
        'moderate': 'moderate_energy',
        'good': 'high_energy',
        'high': 'high_energy',
        'energetic': 'high_energy'
    }
    
    energy_category = energy_map.get(energy_level.lower(), 'moderate_energy')
    suggested_activities = activities[energy_category]
    
    return f"Based on your energy level, I suggest: {', '.join(suggested_activities)}"

# Create tools for the agent
bmi_tool = Tool(
    name="BMI_Calculator",
    description="Calculate BMI when given weight in kg and height in cm. Use this when users ask about BMI or weight status.",
    func=lambda x: calculate_bmi(*[float(i) for i in x.split(',')])
)

calorie_tool = Tool(
    name="Calorie_Calculator", 
    description="Calculate daily calorie needs when given age,weight,height,gender,activity_level separated by commas",
    func=lambda x: calculate_calories(*x.split(','))
)

stress_tool = Tool(
    name="Stress_Assessment",
    description="Assess stress level based on user's description of their current state",
    func=assess_stress_level
)

wellness_tool = Tool(
    name="Wellness_Activities",
    description="Suggest mental wellness activities based on mood and energy level (format: mood,energy_level)",
    func=lambda x: suggest_mental_wellness_activities(*x.split(','))
)

search_tool_wrapped = Tool(
    name="Health_Research",
    description="Search for current health, fitness, or mental wellness information when you need up-to-date data",
    func=search_tool.run
)

# Initialize the agent
tools = [bmi_tool, calorie_tool, stress_tool, wellness_tool, search_tool_wrapped]

# Get the react prompt
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create memory for conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

# Health & Wellness Agent System Prompt
SYSTEM_PROMPT = """
You are a comprehensive AI Health & Mental Wellbeing Agent. You help users with:

1. HEALTH & FITNESS:
   - Personalized diet and fitness plans
   - BMI calculations and health assessments
   - Calorie recommendations
   - Exercise routines and nutrition advice
   
2. MENTAL WELLBEING:
   - Stress level assessment
   - Mental health support and guidance
   - Wellness activity suggestions
   - Emotional support and coping strategies

IMPORTANT GUIDELINES:
- Always be empathetic and supportive
- Provide evidence-based advice
- Suggest professional help when needed
- Use tools when specific calculations are required
- Keep responses practical and actionable
- Maintain a caring, professional tone

If users provide personal health data (age, weight, height, etc.), use the appropriate tools to give personalized recommendations.
For mental health concerns, be supportive but always recommend professional help for serious issues.
"""

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Prepare the input with system prompt
        full_input = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        
        # Get response from agent
        response = agent_executor.invoke({"input": full_input})
        
        return jsonify({
            "response": response["output"],
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e)
        }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation memory"""
    global memory
    memory.clear()
    return jsonify({"message": "Conversation reset successfully"})

if __name__ == '__main__':
    print("🚀 Starting AI Health & Wellbeing Agent...")
    print("💡 Available endpoints:")
    print("   - POST /chat - Send messages to the agent")
    print("   - GET /health - Health check")
    print("   - POST /reset - Reset conversation")
    app.run(debug=True, host='0.0.0.0', port=5000)

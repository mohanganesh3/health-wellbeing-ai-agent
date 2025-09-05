
# Health & Wellbeing AI Agent: Your Personal AI Companion for a Healthier Life

## 🚀 Project Overview

Welcome to the Health & Wellbeing AI Agent, an innovative application designed to provide personalized health advice and support using the power of Artificial Intelligence. This project serves as a robust example of building a full-stack application with a modern React frontend and a scalable Flask backend, integrated with cutting-edge AI capabilities.

Our goal is to create an intelligent assistant that can understand user queries related to health and wellbeing, provide insightful responses, and guide users towards a healthier lifestyle. This README will not only walk you through the project's architecture and implementation but also serve as a comprehensive guide for you to replicate, understand, and even enhance this application from scratch.

## ✨ Core Features

*   **Intelligent Conversational AI**: Powered by Google's Gemini AI, the agent provides natural and context-aware responses to health-related questions.
*   **Responsive User Interface**: A sleek and intuitive frontend built with React, ensuring a seamless experience across various devices (desktop and mobile).
*   **Modular Architecture**: Clear separation of concerns between frontend and backend, promoting maintainability and scalability.
*   **Easy Deployment**: Containerization with Docker and deployment options for platforms like Render.com.
*   **Extensible Design**: Built with future enhancements in mind, such as user authentication, conversation history, and advanced health assessments.

## 🧠 Technical Deep Dive: Unpacking the Architecture

This application follows a classic client-server architecture, with a React-based frontend consuming a RESTful API exposed by a Flask backend. The AI magic happens on the backend, leveraging Google's Generative AI models.

### Frontend Architecture: React, TypeScript, and Vite

The frontend is crafted with React, providing a dynamic and component-based user interface. We use TypeScript for type safety and Vite for an incredibly fast development experience.

**Key Technologies & Patterns:**

*   **React**: For building interactive UI components.
*   **TypeScript**: Enhances code quality and developer productivity through static typing.
*   **Vite**: A next-generation frontend tooling that offers lightning-fast hot module replacement (HMR) and optimized builds.
*   **TailwindCSS**: A utility-first CSS framework for rapidly building custom designs.
*   **React Hooks**: Utilized for managing component state and lifecycle, promoting reusable logic.

**Core Component Structure (Simplified):**

```typescript:/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// The entry point of our React application. It renders the main App component
// into the 'root' DOM element, ensuring strict mode for development checks.
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

The `App.tsx` component orchestrates the main layout and interaction logic, often containing state for messages and handling user input. Components like `ChatWindow`, `MessageInput`, and `Header` would reside here, each responsible for a specific part of the UI.

### Backend Architecture: Flask, Langchain, and Google Gemini

Our backend is a robust Flask application written in Python, designed to act as an intelligent agent. It leverages the power of Langchain to orchestrate interactions with Google's Gemini AI model and various specialized tools. This architecture allows for dynamic and context-aware responses to complex health and wellbeing queries.

**Key Technologies & Patterns:**

*   **Flask**: A micro web framework for Python, providing the foundation for our RESTful API endpoints.
*   **Flask-CORS**: Enables Cross-Origin Resource Sharing, allowing our React frontend to securely communicate with the Flask backend.
*   **Langchain**: A powerful framework for developing applications powered by language models. It facilitates the creation of agents that can intelligently use tools.
*   **Google Generative AI SDK (`langchain_google_genai`)**: Integrates Google's Gemini models into our Langchain agent, enabling advanced conversational AI capabilities.
*   **DuckDuckGo Search (`langchain_community.tools`)**: Provides the agent with real-time search capabilities to fetch up-to-date information.
*   **Custom Tools**: Specialized Python functions wrapped as Langchain tools for specific health and fitness calculations (e.g., BMI, calorie estimation) and mental wellness assessments.
*   **Agent Executor**: The core of our intelligent agent, responsible for deciding which tools to use based on user input and orchestrating the flow of information.
*   **Conversation Buffer Memory**: Maintains chat history, allowing the agent to have context-aware conversations.
*   **Environment Variables**: Securely manages sensitive configurations like API keys.

**Core Backend Logic (`app.py`):**

```python:/backend/app.py
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
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY')

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.3, google_api_key=api_key)
    print("✅ Gemini API connected successfully")
except Exception as e:
    print(f"❌ Error connecting to Gemini API: {e}")

# Initialize tools
search_tool = DuckDuckGoSearchRun()

# Health and Fitness specific tools (simplified for brevity)
def calculate_bmi(weight_kg, height_cm):
    # ... (implementation details)
    pass

def calculate_calories(age, weight, height, gender, activity_level):
    # ... (implementation details)
    pass

# Mental health assessment tools (simplified for brevity)
def assess_stress_level(stress_indicators):
    # ... (implementation details)
    pass

def suggest_mental_wellness_activities(mood, energy_level):
    # ... (implementation details)
    pass

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

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

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
        
        full_input = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        # ... (rest of the chat function logic)
```

### Communication Flow: Frontend to Backend

The frontend communicates with the backend via HTTP requests. When a user sends a message, the React application makes a `POST` request to the `/api/chat` endpoint with the user's message in the request body. The Flask backend then processes this message, interacts with the Gemini AI, and sends the AI's response back to the frontend.

Here's a high-level overview of the system architecture:

```mermaid
graph TD
    A[User 🧑‍💻] -->|Sends Query| B(React Frontend ⚛️)
        React Frontend ⚛️ (Vite, TypeScript, Tailwind CSS) -- API Request (Axios) --> Flask Backend 🐍 (Python, Flask, Gunicorn)
        Flask Backend 🐍 -- Gemini API Call (Google Generative AI SDK) --> Google Gemini AI 🧠
        Google Gemini AI 🧠 -- AI Response (JSON) --> Flask Backend 🐍
        Flask Backend 🐍 -- API Response (JSON) --> React Frontend ⚛️
    B -->|Displays Response| A
```

## 🛠️ Implementation Details & Code Walkthrough

Let's dive into some specific implementations that address key functionalities and challenges.

### AI Response Handling: The `sendMessage` Function

One of the critical aspects of a conversational AI is handling responses efficiently. Our `sendMessage` function in the frontend is responsible for sending user input to the backend and updating the chat interface with the AI's reply.

```typescript:/src/hooks/use-chat.ts
import { useState } from 'react';

interface Message {
  content: string;
  role: 'user' | 'assistant';
}

// This custom hook manages the chat messages state and provides a function to send messages.
export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([])

  const sendMessage = async (message: string) => {
    // Add user's message to the chat immediately for a better UX.
    setMessages((prevMessages) => [...prevMessages, { content: message, role: 'user' }]);

    try {
      // Make a POST request to the backend API with the user's message.
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse the JSON response from the backend.
      const data = await response.json()
      
      // Add the AI's response to the chat messages.
      setMessages((prevMessages) => [...prevMessages, { content: data.response, role: 'assistant' }])
    } catch (error) {
      console.error("Error sending message:", error);
      // Optionally, add an error message to the chat for the user.
      setMessages((prevMessages) => [...prevMessages, { content: "Sorry, I couldn't get a response. Please try again.", role: 'assistant' }]);
    }
  }

  return { messages, sendMessage };
}
```

This `useChat` hook encapsulates the logic for managing chat messages and interacting with the backend, making it reusable across different components.

### Mobile Responsiveness: The `useMobile` Hook

Ensuring a great user experience on all devices is crucial. The `useMobile` hook dynamically detects if the application is being viewed on a mobile device based on screen width, allowing for responsive UI adjustments.

```typescript:/src/hooks/use-mobile.tsx
import { useEffect, useState } from 'react'

// This custom hook determines if the current viewport width indicates a mobile device.
export default function useMobile() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    // Function to check the window width and update the state.
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768) // Common breakpoint for mobile devices
    }
    
    // Add event listener for window resize to re-evaluate mobile status.
    window.addEventListener('resize', checkMobile)
    // Initial check when the component mounts.
    checkMobile()
    
    // Cleanup function: remove the event listener when the component unmounts.
    return () => window.removeEventListener('resize', checkMobile)
  }, []) // Empty dependency array ensures this effect runs only once on mount and cleanup on unmount.

  return isMobile
}
```

This hook can be used in any React component to conditionally render or style elements based on the device type, providing a truly adaptive design.

## 🚀 Getting Started: Build the Project Yourself!

Follow these steps to set up and run the Health & Wellbeing AI Agent on your local machine. This guide assumes you have Node.js (with npm) and Python (with pip) installed.

### Prerequisites

*   **Node.js** (LTS version recommended)
*   **Python 3.9+**
*   **Google AI Studio API Key**: Obtain one from [Google AI Studio](https://aistudio.google.com/)

### Step-by-Step Setup Guide

#### 1. Clone the Repository

First, get the project files onto your local machine:

```bash
git clone https://github.com/your-username/health-wellbeing-ai-agent.git # Replace with actual repo URL
cd health-wellbeing-ai-agent
```

#### 2. Set Up Environment Variables

Create a `.env` file in the `backend` directory to store your Google AI Studio API Key. This is crucial for the backend to communicate with the Gemini model.

```bash
# Create the .env file
touch backend/.env
```

Open `backend/.env` and add your API key:

```
GOOGLE_API_KEY='YOUR_GOOGLE_AI_STUDIO_API_KEY'
```

**Important**: Replace `YOUR_GOOGLE_AI_STUDIO_API_KEY` with your actual key. Do not share this file or commit it to version control!

#### 3. Backend Setup and Run

Navigate to the `backend` directory, install dependencies, and start the Flask server.

```bash
cd backend
pip install -r requirements.txt
python app.py
```

*   The `pip install -r requirements.txt` command installs all necessary Python libraries, including `Flask` and `google-generativeai`.
*   `python app.py` starts the Flask development server, which will typically run on `http://127.0.0.1:5000`.

#### 4. Frontend Setup and Run

Open a **new terminal window**, navigate back to the project root, install frontend dependencies, and start the React development server.

```bash
cd .. # Go back to the project root directory if you are in 'backend'
npm install
npm run dev
```

*   `npm install` fetches all Node.js packages required for the React application.
*   `npm run dev` starts the Vite development server, usually on `http://localhost:5173` (or another available port).

#### 5. Access the Application

Once both the backend and frontend servers are running, open your web browser and navigate to the address provided by the `npm run dev` command (e.g., `http://localhost:5173`). You should now see the Health & Wellbeing AI Agent interface!

### Troubleshooting Common Issues

*   **"Failed to fetch" or Network Errors**: Ensure both your Flask backend (`python app.py`) and React frontend (`npm run dev`) are running simultaneously. Check the terminal outputs for any error messages.
*   **API Key Issues**: Double-check that your `GOOGLE_API_KEY` in `backend/.env` is correct and has the necessary permissions.
*   **Port Conflicts**: If a server fails to start due to a port being in use, you might need to stop the process using that port or configure the application to use a different port.

## ☁️ Deployment Options

This project is designed with deployment flexibility in mind. Here are two primary methods:

### Option 1: Deploying with Render.com

Render.com is a cloud platform that makes it easy to deploy web applications. The provided `render.yaml` configuration simplifies the deployment process for both frontend and backend services.

```yaml
services:
  - name: health-ai-frontend
    type: web
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm run start # Or 'serve -s build' if using a static server
    # Environment variables for frontend if any
    
  - name: health-ai-backend
    type: web
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app # Gunicorn is a production-ready WSGI server
    envVars:
      - key: GOOGLE_API_KEY
        sync: false # Set to true if you want to sync from Render dashboard
        value: YOUR_GOOGLE_AI_STUDIO_API_KEY # Set this securely in Render environment variables
```

To deploy, connect your GitHub repository to Render.com, and it will automatically detect the `render.yaml` file and set up your services.

### Option 2: Containerization with Docker

Docker allows you to package your application and its dependencies into a portable container, ensuring consistent environments across development and production. A `Dockerfile` is provided for building a multi-stage Docker image.

```dockerfile
# Stage 1: Frontend Build
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend Dependencies
FROM python:3.9-alpine as backend-deps
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final Image
FROM nginx:alpine

# Copy frontend build artifacts to Nginx static content directory
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy backend application code and dependencies
WORKDIR /app
COPY --from=backend-deps /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY backend/ /app/backend/

# Expose port 80 for Nginx and 5000 for Flask (though Nginx will proxy to Flask)
EXPOSE 80

# Command to run Nginx and Gunicorn (for Flask) in production
# This setup assumes Nginx is proxying requests to Gunicorn running Flask
CMD sh -c "gunicorn --bind 0.0.0.0:5000 backend.app:app & nginx -g 'daemon off;'"
```

To build and run the Docker image:

```bash
docker build -t health-ai-agent .
docker run -p 80:80 -p 5000:5000 --env GOOGLE_API_KEY='YOUR_KEY' health-ai-agent
```

This Docker setup serves the React frontend via Nginx and runs the Flask backend with Gunicorn, a production-ready WSGI server.

## 🗺️ Future Roadmap

We have exciting plans for the Health & Wellbeing AI Agent:

1.  **User Authentication**: Implement secure user login and registration.
2.  **Conversation History Persistence**: Store and retrieve past conversations for a continuous user experience.
3.  **Expand Health Assessment Capabilities**: Integrate more sophisticated health assessment modules and personalized recommendations.
4.  **Integration with Health APIs**: Connect with external health data sources (e.g., fitness trackers, medical records).
5.  **Voice Interface**: Add speech-to-text and text-to-speech capabilities for a hands-free experience.

## 🤝 Contribution Guidelines

We welcome contributions to make this project even better! If you'd like to contribute, please follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Create a new feature branch** from `main` (e.g., `feature/add-auth`).
    ```bash
    git checkout -b feature/new-component
    ```
3.  **Implement your changes** and ensure all tests pass.
    ```bash
    # Run frontend linting and tests
    npm run lint
    npm test

    # Run backend tests (if any)
    # python -m unittest discover
    ```
4.  **Commit your changes** with clear and concise messages.
5.  **Push your branch** to your forked repository.
6.  **Submit a Pull Request** to the `main` branch of the original repository with a detailed description of your changes.

Thank you for your interest in contributing to the Health & Wellbeing AI Agent!

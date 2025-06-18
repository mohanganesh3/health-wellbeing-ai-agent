
# AI Health & Mental Wellbeing Agent

A comprehensive AI-powered chatbot that combines health & fitness planning with mental wellbeing support, built using Google's Gemini API and LangChain agents.

## 🌟 Features

### Health & Fitness Agent
- **Personalized Diet Plans**: Tailored nutrition recommendations
- **Fitness Planning**: Custom workout routines based on goals
- **BMI Calculator**: Instant BMI calculations and health status
- **Calorie Planning**: Daily calorie needs based on personal metrics
- **Health Research**: Real-time health information lookup

### Mental Wellbeing Agent  
- **Stress Assessment**: Evaluate stress levels and triggers
- **Wellness Activities**: Personalized activity recommendations
- **Mental Health Support**: Empathetic guidance and coping strategies
- **Mood Tracking**: Understanding emotional patterns
- **Professional Referrals**: Guidance when professional help is needed

## 🏗️ Architecture

### Backend (Flask + LangChain)
- **AI Agent Framework**: Multi-tool agent with specialized capabilities
- **Google Gemini Integration**: Free-tier AI model for natural language processing
- **Tool System**: Modular tools for different health domains
- **Memory Management**: Conversation context preservation
- **RESTful API**: Clean endpoints for chat and management

### Frontend (React + TypeScript)
- **Modern UI**: Clean, medical-grade interface design
- **Real-time Chat**: Smooth conversation experience
- **Responsive Design**: Works on all devices
- **Error Handling**: Graceful fallbacks and user feedback
- **Health-focused UX**: Calming colors and professional styling

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
npm install
npm run dev
```

The backend runs on `http://localhost:5000` and frontend on `http://localhost:8080`

## 🔧 API Configuration

The app uses Google's Gemini API (free tier) with the key already configured:
- Model: `gemini-pro`
- Temperature: 0.3 (balanced creativity/accuracy)
- Free tier usage with rate limits

## 📋 API Endpoints

- `POST /chat` - Send messages to the AI agent
- `GET /health` - Backend health check
- `POST /reset` - Reset conversation memory

## 🧠 Agent Capabilities

The AI agent can handle:
1. **Health Calculations**: BMI, daily calories, health assessments
2. **Stress Analysis**: Stress level evaluation and management tips
3. **Activity Recommendations**: Personalized wellness activities
4. **Information Lookup**: Real-time health and wellness research
5. **Supportive Conversations**: Empathetic mental health support

## 💡 Usage Examples

**Health & Fitness:**
- "Calculate my BMI: I'm 25 years old, weigh 70kg, and am 175cm tall"
- "Create a workout plan for weight loss"
- "How many calories should I eat daily?"

**Mental Wellbeing:**
- "I'm feeling overwhelmed and stressed lately"
- "Suggest some relaxation activities for low energy"
- "Help me manage anxiety before presentations"

## 🔒 Privacy & Safety

- No data persistence beyond conversation memory
- Professional help recommendations for serious concerns
- Evidence-based health advice only
- Clear disclaimers about medical limitations

## 🎯 Deployment Ready

- Minimal dependencies for easy deployment
- Docker-ready configuration
- Environment variable configuration
- Production-ready error handling

This is a complete AI health agent system ready for integration and deployment!

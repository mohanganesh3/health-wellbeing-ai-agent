
# AI Health & Mental Wellbeing Agent Backend

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Google API key (already configured in the code):
```bash
export GOOGLE_API_KEY="AIzaSyBuk9yz3u-oBcl3psgCXLs0bu4FSGPyFME"
```

3. Run the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

- `POST /chat` - Send messages to the AI agent
- `GET /health` - Health check endpoint
- `POST /reset` - Reset conversation memory

## Features

- Health & Fitness Planning
- Mental Wellbeing Support
- BMI & Calorie Calculations
- Stress Assessment
- Real-time Health Information Search
- Conversation Memory

## Agent Capabilities

The AI agent can:
1. Calculate BMI and daily calorie needs
2. Assess stress levels and mental state
3. Suggest personalized wellness activities
4. Search for current health information
5. Provide evidence-based health advice
6. Offer mental health support and guidance

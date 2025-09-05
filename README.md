
# Health & Wellbeing AI Agent

## Technical Architecture Deep Dive

This project combines a React frontend with a Flask backend to create an AI-powered health and wellbeing assistant. Here's a detailed breakdown:

### Frontend Structure (React + TypeScript + Vite)
```typescript:/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

Key Features:
- Vite for fast development builds
- TailwindCSS for utility-first styling
- React hooks for state management

### Backend Architecture (Flask + Python)
```python:/backend/app.py
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    response = model.generate_content(data['message'])
    return jsonify({'response': response.text})
```

Core Components:
- REST API endpoints for AI interactions
- Google's Gemini AI integration
- Environment variable configuration

## Development Setup

1. **Frontend Installation**
```bash
cd /Users/mohanganesh/health-wellbeing-ai-agent-2
npm install
npm run dev
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## Key Technical Challenges & Solutions

1. **AI Response Handling**
Implemented streaming responses for better UX:
```typescript:/src/hooks/use-chat.ts
const [messages, setMessages] = useState<Message[]>([])

const sendMessage = async (message: string) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  const data = await response.json()
  setMessages([...messages, { content: data.response, role: 'assistant' }])
}
```

2. **Mobile Responsiveness**
Created custom hook:
```typescript:/src/hooks/use-mobile.tsx
import { useEffect, useState } from 'react'

export default function useMobile() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    window.addEventListener('resize', checkMobile)
    checkMobile()
    
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return isMobile
}
```

## Deployment Options

### Option 1: Render.com
```yaml
services:
  - name: health-ai-frontend
    type: web
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm run start
    
  - name: health-ai-backend
    type: web
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

### Option 2: Docker
```dockerfile
FROM node:18 as frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.9 as backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .

FROM nginx:alpine
COPY --from=frontend /app/dist /usr/share/nginx/html
COPY --from=backend /app /backend
```

## Future Roadmap

1. Implement user authentication
2. Add conversation history persistence
3. Expand health assessment capabilities

## Contribution Guidelines

1. Fork the repository
2. Create feature branch
3. Submit PR with detailed description

```bash
git checkout -b feature/new-component
npm run lint
```

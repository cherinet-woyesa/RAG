# AI Tutor Agent

A comprehensive AI-powered tutoring platform that provides personalized learning experiences for students across various subjects.

## Features

- 🤖 Q&A Chatbot with clear, contextual answers
- 📚 Step-by-step concept explanations
- ✍️ Quiz generation and automatic grading
- 📝 Custom assignments and worksheets
- 💬 Conversational tutoring with friendly engagement
- 🎯 Personalized learning paths
- 📊 Progress tracking and analytics
- 🎤 Voice support for natural interaction

## Tech Stack

### Frontend
- Next.js 14
- Tailwind CSS
- shadcn/ui
- Framer Motion

### Backend
- FastAPI (Python)
- LangChain/LlamaIndex
- OpenAI GPT-4/Claude

### Database
- Supabase (PostgreSQL)
- Pinecone (Vector DB)
- Redis (Caching)

### Additional Services
- Whisper (Speech-to-Text)
- ElevenLabs (Text-to-Speech)
- Strapi (CMS)

## Project Structure

```
ai-tutor/
├── frontend/           # Next.js frontend application
├── backend/           # FastAPI backend services
├── ai-core/          # AI/ML models and services
└── docs/             # Documentation
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker (optional)

### Installation

1. Clone the repository
```bash
git clone [repository-url]
cd ai-tutor
```

2. Set up the frontend
```bash
cd frontend
npm install
npm run dev
```

3. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

4. Set up environment variables
```bash
cp .env.example .env
# Fill in your environment variables
```

## Development

- Frontend runs on: http://localhost:3000
- Backend API runs on: http://localhost:8000
- API documentation: http://localhost:8000/docs

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
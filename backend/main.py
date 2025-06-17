from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai
from fastapi.responses import StreamingResponse

# TODO: Import or implement supabase client
# TODO: Import or implement get_current_user dependency

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Tutor API",
    description="Backend API for the AI Tutor application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Models
class UserProfile(BaseModel):
    name: str
    grade_level: str
    learning_style: str  # "visual", "auditory", "kinesthetic"
    subjects: List[str]  # ["math", "science", "history"]
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None

class Question(BaseModel):
    text: str
    subject: Optional[str] = None
    grade_level: Optional[int] = None

class Answer(BaseModel):
    text: str
    explanation: Optional[str] = None
    related_concepts: Optional[List[str]] = None

class Quiz(BaseModel):
    subject: str
    topic: str
    difficulty: str
    num_questions: int

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"  # easy, medium, hard
    question_type: str = "mixed"  # mcq, short_answer, mixed
    num_questions: int = 5

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AI Tutor API"}

@app.post("/api/chat", response_model=Answer)
async def chat(question: Question):
    try:
        system_message = """You are an AI tutor that helps students learn and understand concepts. \n        When answering questions:\n        1. Provide a clear and concise answer\n        2. Include a detailed explanation that helps the student understand the concept\n        3. List 2-3 related concepts that would help the student build a better understanding\n        Format your response as JSON with fields: text, explanation, and related_concepts"""

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question.text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content
        try:
            import json
            response_data = json.loads(content)
            return Answer(
                text=response_data.get("text", ""),
                explanation=response_data.get("explanation"),
                related_concepts=response_data.get("related_concepts")
            )
        except json.JSONDecodeError:
            return Answer(text=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(question: Question):
    async def event_generator():
        system_message = """You are an AI tutor that helps students learn and understand concepts. \n        When answering questions:\n        1. Provide a clear and concise answer\n        2. Include a detailed explanation that helps the student understand the concept\n        3. List 2-3 related concepts that would help the student build a better understanding\n        Format your response as JSON with fields: text, explanation, and related_concepts"""

        stream = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question.text}
            ],
            temperature=0.7,
            max_tokens=500,
            stream=True
        )
        async for chunk in stream:
            content = chunk['choices'][0]['delta'].get('content', '')
            if content:
                yield content
    return StreamingResponse(event_generator(), media_type="text/plain")

@app.post("/api/profile")
async def update_profile(profile: UserProfile, user: dict = Depends(lambda: None)):
    # TODO: Replace lambda: None with get_current_user when implemented
    try:
        # TODO: Implement supabase logic
        # supabase.table("user_profiles").upsert({...}).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profile")
async def get_profile(user: dict = Depends(lambda: None)):
    # TODO: Replace lambda: None with get_current_user when implemented
    try:
        # TODO: Implement supabase logic
        # response = supabase.table("user_profiles").select("*").eq("user_id", user.id).execute()
        # return response.data[0] if response.data else None
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-quiz", response_model=List[QuizQuestion])
async def generate_quiz(quiz: Quiz):
    try:
        # TODO: Implement quiz generation logic
        return [
            QuizQuestion(
                question="Sample question?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="This is a sample explanation."
            )
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# If you want to use the more advanced quiz generation, uncomment and implement below
# @app.post("/api/generate-quiz")
# async def generate_quiz_advanced(quiz_request: QuizRequest, user: dict = Depends(lambda: None)):
#     # TODO: Replace lambda: None with get_current_user when implemented
#     try:
#         # TODO: Implement supabase and OpenAI logic for personalized quiz
#         return {"quiz": "Generated quiz content here."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
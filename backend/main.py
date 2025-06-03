from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai

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

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AI Tutor API"}

@app.post("/api/chat", response_model=Answer)
async def chat(question: Question):
    try:
        # Create a system message that defines the AI tutor's behavior
        system_message = """You are an AI tutor that helps students learn and understand concepts. 
        When answering questions:
        1. Provide a clear and concise answer
        2. Include a detailed explanation that helps the student understand the concept
        3. List 2-3 related concepts that would help the student build a better understanding
        Format your response as JSON with fields: text, explanation, and related_concepts"""

        # Create the chat completion
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question.text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # Parse the response
        content = response.choices[0].message.content
        
        # Extract the JSON response
        try:
            import json
            response_data = json.loads(content)
            return Answer(
                text=response_data.get("text", ""),
                explanation=response_data.get("explanation"),
                related_concepts=response_data.get("related_concepts")
            )
        except json.JSONDecodeError:
            # If the response is not valid JSON, return it as plain text
            return Answer(text=content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/profile")
async def update_profile(profile: UserProfile, user: dict = Depends(get_current_user)):
    try:
        supabase.table("user_profiles").upsert({
            "user_id": user.id,
            "name": profile.name,
            "grade_level": profile.grade_level,
            "learning_style": profile.learning_style,
            "subjects": profile.subjects,
            "strengths": profile.strengths or [],
            "weaknesses": profile.weaknesses or []
        }).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    try:
        response = supabase.table("user_profiles").select("*").eq("user_id", user.id).execute()
        return response.data[0] if response.data else None
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
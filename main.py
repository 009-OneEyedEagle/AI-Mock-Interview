from fastapi import FastAPI
from routes import start_interview, interview_feedback
import os

app = FastAPI()
app.include_router(start_interview.router)
app.include_router(interview_feedback.router)

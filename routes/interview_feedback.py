from typing import List
from starlette import status
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import google.generativeai as genai
import aiofiles
import os
import fitz 


def configure(): #Loading the env file
    load_dotenv()


configure()
key = os.getenv('api_key') # geting the api key


genai.configure(api_key=key)


router = APIRouter(
    tags=['/report'],
    prefix='/report'
)

UPLOAD_FOLDER = "uploads"
SAVE_FOLDER = "questions"

class Answers( BaseModel) :
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    answer5: str

@router.post("/generate_report")
async def generate_report(Resume_name: str ,ans: Answers):
    # Defining the model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    #getting the questions
    questions_path = os.path.join(SAVE_FOLDER, Resume_name+ ".txt")
    with open(questions_path, "r") as file:
        questions = file.readlines()

    #Getting the resume
    file_path = os.path.join(UPLOAD_FOLDER, Resume_name+ ".pdf")
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)

    prompt = f"""
    
    You are an expert interviewer and report generator.
    You have been provided with the candidate's resume and their answers to the interview questions.
    Generate a detailed interview report based on clarity of answers, appropriate english, relevance to the questions, and overall performance.  
    
    The Resume data is: {text}
    The Questions asked are: {questions}
    The answers provided by the candidate are:
    1. {ans.answer1}
    2. {ans.answer2}
    3. {ans.answer3}
    4. {ans.answer4}
    5. {ans.answer5}

    The report should be only based on the answers provided by the candidate.
    The report should include an analysis of the candidate's strengths and weaknesses, 
    overall performance, and any recommendations for improvement.
    The report should be concise and well-structured.
    And should have a final score out of 100 based on the answers provided.
    The report should be in the format of a paragraph, do not include any additional text or explanation.
    format:
    1. Strengths: 
    2. Weaknesses:
    3. Overall Performance:
    4. Recommendations:
    5. Final Score:
    6. Conclusion:
    """

    response = (model.generate_content(prompt))
    
    if not response.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No report generated")

    return {"report": response.text.strip()}
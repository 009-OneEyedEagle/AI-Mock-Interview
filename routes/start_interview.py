from starlette import status
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, APIRouter
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
    tags=['/start'],
    prefix='/start'
)

UPLOAD_FOLDER = "uploads"
SAVE_FOLDER = "questions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVE_FOLDER, exist_ok=True)


@router.get("/active")
async def active():
    return JSONResponse(content={"message": "The /start endpoint is active"}, status_code=status.HTTP_200_OK)



@router.post("/start_interview")
async def start_interview(resume: UploadFile, interview_type: str = Form(...) ):
    
    #Defining the model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # Check if the file is a PDF
    if not resume.filename.endswith('.pdf'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a PDF")
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    content = await resume.read()
    
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)

    # Decode PDF using PyMuPDF
    doc = fitz.open(stream=content, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    prompt = f""" Extract the relevant information from the resume for {interview_type} interview. 
    The resume text is: {text}
    Return 5 relevent technical questions to ask the candidate based on the resume for the given interview type.
    The questions should be open-ended and designed to assess the candidate's suitability for the role.
    The questions should cover technical skills, problem-solving abilities, and relevant experiences.
    The questions should be tailored to the specific requirements of a {interview_type} interview.
    The questions should be concise and relevant to the candidate's experience and skills.
    The questions should be in the format of a list, each question on a new line.
    If the pdf file is empty or the pdf is not a resume, return "No relevant information found in the resume.
    Be careful if the resume is empty or not a resume, do not generate random questions, just return "No relevant information found in the resume".
    You can also ask to write short code snippets if the interview type is related to coding or sql commands if the interview type is related to databases.
    If there is no sufficient information or the given resume type is not present in the resume, ask general technical interview questions about {interview_type}.
    #Example:
    If the interview type is "DevOps" and the resume does not contain any or very little information about DevOps, return general technical questions about DevOps, like "What is CI/CD pipelines, several lunix commands, etc.
    
    Don't ask questions on a project if it is not of the given interview type.
    Return the questions only, do not include any additional text or explanation.
    
    """

    response = (model.generate_content(prompt))
        
    # Split the text into lines
    lines = response.text.strip().split("\n")

    # Filter non-empty lines and remove the '* ' or numbering
    questions = [line.lstrip("* ").strip() for line in lines if line.strip()]

    # Map to dictionary format: {'question 1': ..., ...}
    formatted_questions = {f"question {i+1}": question for i, question in enumerate(questions)}

    #Saving the questions to a file
    save_path = os.path.join(SAVE_FOLDER, f"{resume.filename[:-4]}.txt")
    with open(save_path, 'w') as f:
        for question in formatted_questions.values():
            f.write(question + "\n")

    response = {
        "questions": formatted_questions,
        "resume_text": text,
    }
    return response

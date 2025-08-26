# Mock Mate – Personalized AI Mock Interview Platform

**Mock Mate** is an AI-powered mock interview platform that provides personalized interview practice tailored to a candidate's resume and chosen interview type. It evaluates responses and generates a detailed feedback report highlighting strengths, weaknesses, recommendations, and a performance score — making interview preparation more accessible, affordable, and effective.

---

## 🚀 Features
- **Resume-Based Question Generation** – Custom interview questions derived from the candidate's own resume.
- **Multiple Interview Types** – Technical, HR, behavioral, and more.
- **Automated Feedback Report** – Strengths, weaknesses, recommendations, and a score.
- **Accessibility** – Practice interviews anytime, anywhere.
- **Future-Ready** – Plans for voice-based interviews, resume analyzer, and email integration.

---

## 📌 Problem Statement
Many job seekers lack access to quality, personalized interview preparation tools. Existing solutions are often:
- Generic and untailored to an individual's profile.
- Expensive or inaccessible in remote areas.
- Limited in actionable feedback.

**Mock Mate** aims to bridge this gap by offering scalable, AI-driven, and affordable interview coaching aligned with *Quality Education* (SDG 4).

---

## 🎯 Objectives
- Deliver **personalized interview preparation** for better employability.
- Provide **actionable performance feedback** for continuous improvement.
- Make **interview coaching accessible** to students, job seekers, and professionals worldwide.

---

## 🛠 Tech Stack
- **Backend:** Python, FastAPI
- **AI/ML:** LangChain, Google Gemini LLM
- **OCR:** PyTesseract
- **Frontend:** HTML, CSS, JavaScript
- **Integration:** API-based communication between frontend and backend

---

## ⚙️ How It Works
1. **Upload Resume** – The system extracts text using OCR.
2. **Select Interview Type** – Technical, HR, or behavioral.
3. **Get Questions** – AI generates personalized questions from the resume.
4. **Answer** – Candidate types in responses.
5. **Receive Feedback** – AI evaluates and generates a structured performance report.

---

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mock-mate.git
   cd mock-mate
2. **Install dependencies**
```pip install -r requirements.txt```

3. **Run the FastAPI server**
```uvicorn main:app --reload```

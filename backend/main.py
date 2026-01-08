from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/generate-quiz")
def generate_quiz(url: str):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"}  # ✅ IMPORTANT
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ SAFE TITLE EXTRACTION
        title_tag = soup.find("h1")
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "Wikipedia Topic"

        # ✅ SAFE PARAGRAPH EXTRACTION
        paragraphs = soup.find_all("p")
        content = ""
        for p in paragraphs:
            if p.text.strip():
                content += p.text.strip() + " "
            if len(content) > 300:
                break

        quiz = {
            "topic": title,
            "questions": [
                {
                    "question": f"Who is {title}?",
                    "answer": content[:300]
                }
            ]
        }

        return quiz

    except Exception as e:
        return {"error": str(e)}

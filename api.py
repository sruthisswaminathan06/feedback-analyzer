import os
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

app = FastAPI(title="Customer Feedback Analyzer API")

class Review(BaseModel):
    text: str = Field(..., description="The raw customer review text.")

class Analysis(BaseModel):
    label: Literal["positive", "negative", "neutral"] = Field(
        ..., description="Overall sentiment classification."
    )
    score: int = Field(
        ..., ge=1, le=5, description="Sentiment rating from 1 (worst) to 5 (best)."
    )
    theme: str = Field(
        ..., description="Primary topic or feature mentioned."
    )

@app.post("/analyze", response_model=Analysis)
def analyze_review(review: Review):
    if not review.text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")

    system_prompt = (
        "You are an expert sentiment analysis assistant. Analyze the provided customer review. "
        "Determine the overall sentiment label (positive, negative, neutral), assign a score from 1 to 5, "
        "and categorize the main topic into a single theme phrase."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Customer Review: {review.text}",
            config={
                "system_instruction": system_prompt,
                "response_mime_type": "application/json",
                "response_schema": Analysis,
            },
        )
        structured_analysis = Analysis.model_validate_json(response.text)
        return structured_analysis

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calling the AI service: {str(e)}"
        )
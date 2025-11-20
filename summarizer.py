import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Dict, Any, List

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# --- Pydantic Schema for Structured Output ---

class PaperSummary(BaseModel):
    """Schema for a single academic paper summary."""
    title: str = Field(description="The original title of the academic paper.")
    summary: str = Field(description="A concise, academic-quality summary of the paper's key contributions, methods, and results.")
    key_findings: List[str] = Field(description="A list of 3-5 of the most important findings or conclusions.")
    relevance_to_topic: str = Field(description="A brief explanation of why this paper is relevant to the main research topic.")
    original_url: str = Field(description="The Semantic Scholar URL for the paper.")


class LiteratureReviewOutput(BaseModel):
    """The main schema for the final literature review section."""
    topic: str = Field(description="The research topic provided by the user.")
    overview: str = Field(description="A brief, academic introduction and synthesis of the topic based on the papers reviewed.")
    individual_summaries: List[PaperSummary] = Field(description="A list of structured summaries for each paper.")


# --- Gemini Client and Summarization Function ---

GEMINI_MODEL = "gemini-2.5-flash"
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

def generate_summary(paper_metadata: List[Dict[str, Any]], topic: str) -> LiteratureReviewOutput | None:
    """
    Uses Gemini to summarize the paper abstracts and consolidate the results 
    into a structured Pydantic object (RAG Core).
    """
    if not client:
        print("Gemini client not initialized. Cannot summarize.")
        return None

    # Format the retrieved papers into a single context string
    paper_texts = "\n\n---\n\n".join([
        f"Title: {p['title']}\nAbstract: {p['abstract']}\nURL: {p['url']}"
        for p in paper_metadata
    ])
    
    if not paper_texts.strip():
        print("No paper metadata provided for summarization.")
        return None

    system_prompt = (
        "You are an expert Academic Research Assistant. Your task is to process a list of academic papers "
        "and generate a consolidated, high-quality, structured literature review. The tone must be formal and academic. "
        "The primary topic for the review is: '{topic}'. "
        "Ensure the 'summary' and 'overview' fields are detailed and insightful."
    ).format(topic=topic)
    
    user_prompt = f"""
    Please analyze the following academic papers retrieved for the topic: "{topic}".
    
    You must generate the complete output following the required JSON schema.
    
    --- PAPERS TO REVIEW (Metadata/Abstracts) ---
    {paper_texts}
    """
    
    print(f"🧠 Generating consolidated review using {GEMINI_MODEL}...")
    
    try:
        # Configure for structured JSON output using the Pydantic schema
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=LiteratureReviewOutput,
        )
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[user_prompt],
            config=config,
        )
        
        review_data = LiteratureReviewOutput.model_validate_json(response.text)
        
        print("✅ Review generation complete.")
        return review_data

    except Exception as e:
        print(f"❌ Error during Gemini API call or structured output parsing: {e}")
        return None
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

# Define the Router instance
router = APIRouter(
    prefix="/api/text",
    tags=["Text Tools"],
    responses={404: {"description": "Not found"}}
)

# Request/Response Models
class TextInput(BaseModel):
    text: str
    options: Optional[Dict] = None

class TextResponse(BaseModel):
    result: str
    original: str
    operation: str

class TextAnalysis(BaseModel):
    word_count: int
    character_count: int
    sentence_count: int
    reading_time: str

# Text Tools Endpoints

@router.post("/uppercase", response_model=TextResponse)
async def to_uppercase(request: TextInput) -> TextResponse:
    """Converts the input text to all uppercase letters."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    return {
        "result": request.text.upper(),
        "original": request.text,
        "operation": "uppercase"
    }

@router.post("/lowercase", response_model=TextResponse)
async def to_lowercase(request: TextInput) -> TextResponse:
    """Converts the input text to all lowercase letters."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    return {
        "result": request.text.lower(),
        "original": request.text,
        "operation": "lowercase"
    }

@router.post("/reverse", response_model=TextResponse)
async def reverse_text(request: TextInput) -> TextResponse:
    """Reverses the order of characters in the input text."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    return {
        "result": request.text[::-1],
        "original": request.text,
        "operation": "reverse"
    }

@router.post("/title-case", response_model=TextResponse)
async def title_case(request: TextInput) -> TextResponse:
    """Converts text to title case."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    return {
        "result": request.text.title(),
        "original": request.text,
        "operation": "title_case"
    }

@router.post("/word-count", response_model=TextAnalysis)
async def word_count(request: TextInput) -> TextAnalysis:
    """Analyzes text and returns word count, character count, etc."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    words = len(request.text.split())
    characters = len(request.text)
    sentences = request.text.count('.') + request.text.count('!') + request.text.count('?')
    reading_time = f"{max(1, words // 200)} min"
    
    return {
        "word_count": words,
        "character_count": characters,
        "sentence_count": sentences,
        "reading_time": reading_time
    }

@router.post("/remove-spaces", response_model=TextResponse)
async def remove_spaces(request: TextInput) -> TextResponse:
    """Removes all spaces from the text."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    return {
        "result": request.text.replace(" ", ""),
        "original": request.text,
        "operation": "remove_spaces"
    }

@router.post("/slugify", response_model=TextResponse)
async def slugify_text(request: TextInput) -> TextResponse:
    """Converts text to URL-friendly slug."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    slug = (request.text.lower()
            .replace(" ", "-")
            .replace("_", "-")
            .replace(".", "-")
            .replace(",", ""))
    
    # Remove multiple consecutive hyphens
    while "--" in slug:
        slug = slug.replace("--", "-")
    
    return {
        "result": slug.strip("-"),
        "original": request.text,
        "operation": "slugify"
    }

# Get all available text operations
@router.get("/operations")
async def get_operations():
    """Returns list of all available text operations."""
    return {
        "operations": [
            {"name": "uppercase", "description": "Convert text to uppercase"},
            {"name": "lowercase", "description": "Convert text to lowercase"},
            {"name": "reverse", "description": "Reverse the text"},
            {"name": "title_case", "description": "Convert to title case"},
            {"name": "word_count", "description": "Analyze text statistics"},
            {"name": "remove_spaces", "description": "Remove all spaces"},
            {"name": "slugify", "description": "Convert to URL-friendly slug"}
        ]
    }

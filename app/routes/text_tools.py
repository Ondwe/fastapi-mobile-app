from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter(tags=["Text Tools"])

@router.get("/text-tools")
async def text_tools_home():
    return {"message": "Text Tools API"}

@router.get("/text/reverse")
async def reverse_string(text: str):
    return {"original": text, "reversed": text[::-1]}

@router.get("/text/uppercase")
async def uppercase_string(text: str):
    return {"original": text, "uppercase": text.upper()}

@router.get("/text/lowercase")
async def lowercase_string(text: str):
    return {"original": text, "lowercase": text.lower()}

@router.get("/text/word-count")
async def word_count(text: str):
    words = text.split()
    return {"text": text, "word_count": len(words), "character_count": len(text)}

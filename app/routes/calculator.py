from fastapi import APIRouter, HTTPException, Depends
from app.auth import get_current_user

router = APIRouter(tags=["Calculator"])

@router.get("/calculator")
async def calculator_home():
    return {"message": "Calculator API"}

@router.get("/advanced-calculator/{expression}")
async def advanced_calculator(expression: str, current_user: dict = Depends(get_current_user)):
    """Advanced calculator with premium features"""
    try:
        # Simple safe evaluation (in production, use a proper math parser)
        # This is a simplified version - be very careful with eval in production!
        safe_expression = expression.replace(" ", "").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ")
        
        # For demo purposes, just return a mock result
        result = f"Calculated: {expression} = 42 (demo)"
        
        return {"result": result, "expression": expression, "user": current_user["username"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@router.get("/calc/add")
async def add_numbers(a: float, b: float):
    return {"result": a + b}

@router.get("/calc/subtract")
async def subtract_numbers(a: float, b: float):
    return {"result": a - b}

@router.get("/calc/multiply")
async def multiply_numbers(a: float, b: float):
    return {"result": a * b}

@router.get("/calc/divide")
async def divide_numbers(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}

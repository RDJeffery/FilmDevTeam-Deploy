import logging
import os
from typing import List
from pathlib import Path
from fastapi.staticfiles import StaticFiles

import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
import gradio as gr
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables first
load_dotenv()

# Set environment variables
APP_TOKEN = os.getenv("APP_TOKEN")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from FilmDevAgency.agency import agency
from utils.demo_gradio_override import demo_gradio_override

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI application
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize email monitoring when the application starts"""
    try:
        # Log available agents
        logging.info("Initializing agency...")
        if hasattr(agency, 'agents'):
            agent_names = [agent.name for agent in agency.agents]
            logging.info(f"Available agents: {agent_names}")
            
            # Find the Creative Director agent
            creative_director = next((agent for agent in agency.agents if agent.name == "Creative Director"), None)
            if creative_director:
                logging.info("Found Creative Director agent, starting email monitoring...")
                creative_director.start_email_monitoring()
                logging.info("Email monitoring started successfully")
            else:
                logging.error("Could not find Creative Director agent in agency.agents")
                logging.error(f"Available agents: {agent_names}")
        else:
            logging.error("Agency has no agents attribute")
    except Exception as e:
        logging.error(f"Failed to start email monitoring: {str(e)}")
        logging.error("Agency state:", exc_info=True)

# Create static directories if they don't exist
static_dir = Path("src/static")
assets_dir = static_dir / "assets"
for dir_path in [static_dir, assets_dir]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")

# CORS Configuration
# For local development, allow all origins
origins = ["*"]
# For production, use specific origins:
# origins = [
#     "https://your-generated-Railway-domain.up.railway.app",  # Your Railway domain
#     "http://localhost:8000",  # Local development
# ]

# Add CORS middleware to enable cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Override the demo_gradio function
agency.demo_gradio = demo_gradio_override
# Mount the gradio interface with basic auth
gradio_interface = agency.demo_gradio(agency)
app = gr.mount_gradio_app(
    app, 
    gradio_interface, 
    path="/demo-gradio",
    auth=(os.getenv("GRADIO_USERNAME", "admin"), os.getenv("GRADIO_PASSWORD", "admin"))  # Use env vars with defaults
)

security = HTTPBearer()


# Models
class AttachmentTool(BaseModel):
    type: str


class Attachment(BaseModel):
    file_id: str
    tools: List[AttachmentTool]


class AgencyRequest(BaseModel):
    message: str
    attachments: List[Attachment] = []


# Token verification
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != APP_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


# API endpoint
@app.post("/api/agency")
async def get_completion(request: AgencyRequest, token: str = Depends(verify_token)):
    response = agency.get_completion(
        request.message,
        attachments=request.attachments,
    )
    return {"response": response}


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Global exception handler to return formatted error responses"""
    error_message = str(exc)
    if isinstance(exc, tuple):
        error_message = str(exc[1]) if len(exc) > 1 else str(exc[0])

    return JSONResponse(status_code=500, content={"error": error_message})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

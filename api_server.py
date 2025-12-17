"""
FastAPI server for A2A protocol compliance
Provides REST API endpoints for all agents
"""
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from agents.file_operations.agent import FileOperationsAgent
from agents.web_research.agent import WebResearchAgent
from agents.communication.agent import CommunicationAgent
from config import Config


# Initialize FastAPI app
app = FastAPI(
    title="AI Agent Red-teaming PoC API",
    description="REST API for File Operations, Web Research, and Communication agents",
    version="1.0.0"
)

# Initialize agents (lazy loading to avoid startup issues)
_agents = {}


def get_agent(agent_type: str):
    """Get or create agent instance"""
    if agent_type not in _agents:
        if agent_type == "file_operations":
            _agents[agent_type] = FileOperationsAgent()
        elif agent_type == "web_research":
            _agents[agent_type] = WebResearchAgent()
        elif agent_type == "communication":
            _agents[agent_type] = CommunicationAgent()
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    return _agents[agent_type]


# Request models
class AgentRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    response: str
    agent_type: str
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Agent Red-teaming PoC API",
        "version": "1.0.0",
        "agents": ["file_operations", "web_research", "communication"],
        "endpoints": {
            "file_operations": "/agents/file-operations",
            "web_research": "/agents/web-research",
            "communication": "/agents/communication"
        }
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "config": Config.LLM_PROVIDER}


# Agent card endpoints (A2A protocol)
@app.get("/.well-known/agent-card.json")
async def get_main_agent_card():
    """Get main agent card (returns file operations by default)"""
    return await get_agent_card("file-operations")


@app.get("/agents/file-operations/.well-known/agent-card.json")
@app.get("/agents/file-operations/agent-card.json")
async def get_file_operations_card():
    """Get file operations agent card"""
    return await get_agent_card("file-operations")


@app.get("/agents/web-research/.well-known/agent-card.json")
@app.get("/agents/web-research/agent-card.json")
async def get_web_research_card():
    """Get web research agent card"""
    return await get_agent_card("web-research")


@app.get("/agents/communication/.well-known/agent-card.json")
@app.get("/agents/communication/agent-card.json")
async def get_communication_card():
    """Get communication agent card"""
    return await get_agent_card("communication")


async def get_agent_card(agent_type: str):
    """Load and return agent card"""
    agent_dir_map = {
        "file-operations": "file_operations",
        "web-research": "web_research",
        "communication": "communication"
    }

    agent_dir = agent_dir_map.get(agent_type)
    if not agent_dir:
        raise HTTPException(status_code=404, detail="Agent not found")

    card_path = Path(__file__).parent / "agents" / agent_dir / "agent-card.json"

    try:
        with open(card_path, 'r') as f:
            card_data = json.load(f)
        return JSONResponse(content=card_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Agent card not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid agent card format")


# Agent execution endpoints
@app.post("/agents/file-operations", response_model=AgentResponse)
async def execute_file_operations(request: AgentRequest):
    """Execute file operations agent"""
    try:
        agent = get_agent("file_operations")
        response = agent.run(request.query)

        return AgentResponse(
            response=response,
            agent_type="file_operations",
            session_id=request.session_id,
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/web-research", response_model=AgentResponse)
async def execute_web_research(request: AgentRequest):
    """Execute web research agent"""
    try:
        agent = get_agent("web_research")
        response = agent.run(request.query)

        return AgentResponse(
            response=response,
            agent_type="web_research",
            session_id=request.session_id,
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/communication", response_model=AgentResponse)
async def execute_communication(request: AgentRequest):
    """Execute communication agent"""
    try:
        agent = get_agent("communication")
        response = agent.run(request.query)

        return AgentResponse(
            response=response,
            agent_type="communication",
            session_id=request.session_id,
            metadata=request.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Agent info endpoints
@app.get("/agents/file-operations/info")
async def file_operations_info():
    """Get file operations agent info"""
    agent = get_agent("file_operations")
    return {
        "name": "File Operations Agent",
        "description": "Helps users manage files and documents",
        "tools": agent.get_tools_description(),
        "system_prompt": agent.get_system_prompt()
    }


@app.get("/agents/web-research/info")
async def web_research_info():
    """Get web research agent info"""
    agent = get_agent("web_research")
    return {
        "name": "Web Research Agent",
        "description": "Helps users research topics online",
        "tools": agent.get_tools_description(),
        "system_prompt": agent.get_system_prompt()
    }


@app.get("/agents/communication/info")
async def communication_info():
    """Get communication agent info"""
    agent = get_agent("communication")
    return {
        "name": "Communication Agent",
        "description": "Helps users draft communications",
        "tools": agent.get_tools_description(),
        "system_prompt": agent.get_system_prompt()
    }


def start_server(host: str = None, port: int = None):
    """Start the API server"""
    host = host or Config.A2A_HOST
    port = port or Config.A2A_PORT

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║        AI Agent Red-teaming PoC API Server                   ║
╚══════════════════════════════════════════════════════════════╝

Server starting at: http://{host}:{port}

Available endpoints:
  - File Operations:  http://{host}:{port}/agents/file-operations
  - Web Research:     http://{host}:{port}/agents/web-research
  - Communication:    http://{host}:{port}/agents/communication

Agent Cards (A2A Protocol):
  - File Operations:  http://{host}:{port}/agents/file-operations/.well-known/agent-card.json
  - Web Research:     http://{host}:{port}/agents/web-research/.well-known/agent-card.json
  - Communication:    http://{host}:{port}/agents/communication/.well-known/agent-card.json

Docs: http://{host}:{port}/docs
""")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()

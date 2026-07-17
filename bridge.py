"""HTTP bridge for exposing selected MCP tools as REST endpoints."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from intune_mcp_server.server import (
    get_intune_overview,
    list_managed_devices,
    test_connection,
)


app = FastAPI(title="Intune MCP HTTP Bridge", version="1.0.0")


class ListDevicesRequest(BaseModel):
    filter_query: str = Field(default="")
    top: int = Field(default=50, ge=1, le=1000)


@app.get("/")
async def root() -> dict:
    return {
        "service": "intune-mcp-bridge",
        "status": "ok",
        "endpoints": [
            "GET /health",
            "POST /actions/test-connection",
            "POST /actions/get-intune-overview",
            "POST /actions/list-managed-devices",
        ],
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/actions/test-connection")
async def action_test_connection() -> dict:
    try:
        return await test_connection()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/actions/get-intune-overview")
async def action_get_intune_overview() -> dict:
    try:
        return await get_intune_overview()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/actions/list-managed-devices")
async def action_list_managed_devices(payload: ListDevicesRequest) -> dict:
    try:
        return await list_managed_devices(
            filter_query=payload.filter_query,
            top=payload.top,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

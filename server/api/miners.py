from fastapi import APIRouter, WebSocket, BackgroundTasks
import asyncio
from .db import get_miner_list, start_scan, export_report

router = APIRouter()

@router.get("/miners")
async def list_miners():
    return get_miner_list()

@router.post("/scan")
async def scan_miners(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_scan)
    return {"msg": "Scan started"}

@router.get("/export")
async def export(format: str = "csv"):
    return export_report(format)

@router.websocket("/ws/miners")
async def miners_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        miners = get_miner_list()
        await websocket.send_json(miners)
        await asyncio.sleep(2)
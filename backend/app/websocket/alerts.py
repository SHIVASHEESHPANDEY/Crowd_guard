from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import connection_manager


router = APIRouter(tags=["websocket"])


@router.websocket("/ws/alerts")
async def alerts_socket(websocket: WebSocket) -> None:
    await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

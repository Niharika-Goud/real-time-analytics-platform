from fastapi import WebSocket


# Manages active WebSocket client connections
class ConnectionManager:

    def __init__(self):

        # Store all connected WebSocket clients
        self.active_connections = []


    # Accept and register new WebSocket connection
    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        self.active_connections.append(websocket)


    # Remove disconnected WebSocket client
    def disconnect(self, websocket: WebSocket):

        self.active_connections.remove(websocket)


    # Broadcast live event data to all connected clients
    async def broadcast(self, message: dict):

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(message)

            except Exception:

                disconnected.append(connection)

        for conn in disconnected:

            self.disconnect(conn)


# Shared WebSocket connection manager instance
manager = ConnectionManager()
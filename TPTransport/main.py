"""Entry point for the bus-tracking server.

Run in development:
    python main.py

Run in production (recommended):
    uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --workers 1

Note: use a single worker — the WebSocket broadcaster and offline-detector
are in-process asyncio tasks; multiple workers would each run their own
broadcast loop and would not share connection state.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,   # set to True for local development
        log_level="info",
    )

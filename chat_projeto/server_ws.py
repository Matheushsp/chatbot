import os
import asyncio
import websockets

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

connected = set()

async def handler(ws):
    connected.add(ws)
    try:
        async for msg in ws:
            for c in connected:
                if c != ws:
                    await c.send(msg)
    finally:
        connected.remove(ws)

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Servidor WS em ws://{HOST}:{PORT}")
        await asyncio.Future()  # Mantém rodando

asyncio.run(main())
